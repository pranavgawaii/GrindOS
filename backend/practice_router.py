import json
import os
import re
import base64
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from judge0_router import execute_on_judge0, parse_driver_results

router = APIRouter()

class PracticeRequest(BaseModel):
    problem: str
    language: str
    constraints: str = ""
    userAttempt: str = ""
    environment: str = "auto"
    verbosity: str = "detailed"
    verify_code: bool = True
    isCompletionMode: bool = False
    starterCode: str = ""
    completionOutputFormat: str = "snippet"
    attemptedFirst: bool = False
    model: str = "gemini"
    errorMessage: str = ""

class ExtractTextRequest(BaseModel):
    image_base64: str

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Failed to initialize Supabase: {e}")

async def ask_gemini_json(system_prompt: str, user_message: str, model_choice: str = "gemini") -> dict:
    import asyncio
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set.")

    def _call_llm():
        if model_choice.startswith("claude"):
            model_map = {
                "claude-3-5-sonnet": {
                    "anthropic": "claude-3-5-sonnet-20241022",
                    "openrouter": "anthropic/claude-sonnet-4"
                },
                "claude-3-5-haiku": {
                    "anthropic": "claude-3-5-haiku-20241022",
                    "openrouter": "anthropic/claude-3.5-haiku"
                },
                "claude-3-opus": {
                    "anthropic": "claude-3-opus-20240229",
                    "openrouter": "anthropic/claude-opus-4"
                }
            }
            choice_info = model_map.get(model_choice, model_map["claude-3-5-sonnet"])
            
            anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
            if anthropic_key:
                try:
                    from anthropic import Anthropic
                    client = Anthropic(api_key=anthropic_key)
                    response = client.messages.create(
                        model=choice_info["anthropic"],
                        max_tokens=4000,
                        system=system_prompt,
                        messages=[{"role": "user", "content": user_message}]
                    )
                    return response.content[0].text
                except Exception as e:
                    print(f"Anthropic Claude API failed: {e}. Trying OpenRouter Claude...")
            
            openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
            if openrouter_key:
                try:
                    import openai
                    client = openai.OpenAI(
                        base_url="https://openrouter.ai/api/v1",
                        api_key=openrouter_key,
                    )
                    response = client.chat.completions.create(
                        model=choice_info["openrouter"],
                        max_tokens=2000,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ]
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    print(f"OpenRouter Claude fallback failed: {e}. Falling back to default Gemini/Llama pipeline...")

        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.2,
                    response_mime_type="application/json"
                ),
            )
            return response.text
        except Exception as e:
            print(f"Gemini failed in analysis: {e}. Falling back to Groq Llama 3.3 70B...")
            
        try:
            from groq import Groq
            groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
            groq_response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            return groq_response.choices[0].message.content
        except Exception as groq_err:
            print(f"Groq fallback failed: {groq_err}. Falling back to OpenRouter free tier...")
            import openai
            openai_client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.environ.get("OPENROUTER_API_KEY", ""),
            )
            free_models = [
                "qwen/qwen3-coder:free",
                "google/gemma-4-31b-it:free",
                "meta-llama/llama-3.3-70b-instruct:free",
                "openrouter/free"
            ]
            last_openrouter_err = None
            for fallback_model in free_models:
                try:
                    print(f"Trying OpenRouter free model: {fallback_model}...")
                    openrouter_response = openai_client.chat.completions.create(
                        model=fallback_model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ]
                    )
                    return openrouter_response.choices[0].message.content
                except Exception as openrouter_err:
                    last_openrouter_err = openrouter_err
                    print(f"OpenRouter {fallback_model} failed: {openrouter_err}")
                    continue
            raise last_openrouter_err

    try:
        content = await asyncio.to_thread(_call_llm)
        # Ensure we strip any markdown blocks if the LLM adds them despite response_mime_type
        content = re.sub(r"^```json\s*", "", content, flags=re.IGNORECASE|re.MULTILINE)
        content = re.sub(r"^```\s*", "", content, flags=re.MULTILINE)
        return json.loads(content.strip())
    except Exception as e:
        print(f"Gemini JSON Error: {e}")
        try:
            print(f"Raw output: {content}")
        except:
            pass
        raise Exception(f"Failed to generate analysis: {str(e)}")

def build_system_prompt(language: str, environment: str, verbosity: str, is_completion: bool = False, starter_code: str = "", output_format: str = "snippet", is_error_fix: bool = False) -> str:
    env_instruction = ""
    if environment == "leetcode":
        env_instruction = "Provide a class/function template (LeetCode style) containing the core solution logic. At the top of the file, include necessary standard library imports/headers (e.g. '#include <vector>' or 'from typing import List'). At the bottom of the file, write a simple human-style main execution block (e.g., 'if __name__ == \"__main__\":' in Python, or a standard 'int main()' in C++) that initializes the class, calls the function with a sample test case, and prints the result to standard output so that it is instantly executable in a terminal."
    elif environment == "oa":
        env_instruction = (
            "Provide a pure sys.stdin/stdout flat script (OA style) that writes all imports, parsing, solution, and stdout prints at the root level. "
            "To be 100% robust and pass all test cases on various online assessment platforms, the parsing logic MUST be resilient. "
            "Specifically for Python, read standard input and attempt to parse it as JSON using 'json.loads' inside a try-except block. "
            "If it parses as a dictionary (e.g. {'n': 8456986}), extract the value (e.g., data.get('n', data.get('x', list(data.values())[0]))); "
            "if it parses as a list or a single value, use it directly. "
            "If the JSON parsing fails (throws an exception) or the input is empty/plain text, catch the exception and fall back to standard text-based parsing "
            "methods (like sys.stdin.read().split() or sys.stdin.readline().strip() mapped to int/float/string). "
            "This resilient approach allows the script to pass test cases on both JSON-passing sandboxes and standard raw-text terminals. "
            "Do NOT wrap the core logic inside a class or nested solve functions, and do NOT include any main guard block."
        )
    else:
        # Default/Auto format selection per SKILL.md guidelines
        env_instruction = (
            "Automatically select the code structure format based on the problem statement context. "
            "1. If the problem statement mentions standard input, stdin, or reading lines/input, write a flat sys.stdin/stdout script (OA style) "
            "with resilient parsing logic: in Python, try to parse input as JSON using 'json.loads' inside a try-except block (if it's a dict like {'n': 8456986}, "
            "extract the key value; if a list/integer, use it). If it fails or is raw text, fall back to standard text parsing (sys.stdin.read().split() "
            "or sys.stdin.readline().strip()). This makes the script run perfectly on both JSON-input platforms and normal terminal streams. "
            "2. Otherwise, write a class/function template (LeetCode style) wrapped in a Solution class. "
            "In both cases, ensure the file has all standard imports/headers at the top."
        )

    completion_instruction = ""
    if is_completion:
        completion_instruction = f"""
The user has provided a starter code / stub with blanks/TODOs/comments. 
Starter Code / Stub:
{starter_code}

You MUST generate the missing code to fill the blanks/TODOs.
CRITICAL FORMATTING & REASONING RULES FOR COMPLETION MODE:
1. BEFORE WRITING THE CODE, carefully analyze:
   - The exact function/class signatures and any import statements.
   - The parameter and return types (e.g. typing or type hints, if any) to align with them perfectly.
   - Surrounding variable names, bindings, helper methods, and overall coding style.
2. DO NOT rewrite, rename, or alter the style of the existing starter code. Keep everything else intact.
3. Make sure the generated solution integrates seamlessly into the provided stub without introducing compilation, syntax, or runtime errors.
4. If the output format is "snippet":
   - Return ONLY the missing lines/code snippet in the "solutionCode" field of the JSON.
   - In the "explanation" field, start with a clear, step-by-step guide on exactly where and how to insert this snippet (e.g. line numbers or code blocks to search for).
5. If the output format is "full":
   - Return the ENTIRE completed file with all blanks/TODOs filled in the "solutionCode" field.
6. Keep the solution code fully humanized and consistent with the target language ({language}).
"""

    error_fix_instruction = ""
    if is_error_fix:
        error_fix_instruction = f"""
CRITICAL ERROR DEBUGGING & FIXING RULES:
The user is reporting an execution, compilation, or runtime error with the code provided in the user attempt (which is the previous generated code).
1. Carefully analyze the error message/stack trace and the previous code attempt to pinpoint the bug.
2. In the "explanation" field, explain exactly what was causing the root bug and how you fixed it.
3. Write the fully corrected optimal code in the "solutionCode" field.
4. Ensure the new code has NO errors, handles boundary/edge cases safely, and respects all constraints.
"""

    return f"""You are an elite competitive programming coach and AI software engineer. 
The user will provide a DSA problem, their target language ({language}), optionally user constraints/requirements, and optionally their attempt.

You must return a raw JSON object with EXACTLY the following structure. ENSURE ALL CODE STRINGS ARE PROPERLY ESCAPED FOR JSON (e.g., escape double quotes as \\" and newlines as \\n):
{{
  "solutionCode": "Write the final optimal code in {language}. CRITICAL HUMANIZATION RULES: 1. Use clean, elegant variable names that are concise but meaningful (e.g. n, m, res, ans, dp, cnt, loop index variables like i, j, or pointers like l, r or left, right). Do NOT use excessively verbose names (like indexLeftPointer), and do NOT use single-character variables to the point of being unreadable. 2. Absolutely NO comments or docstrings explaining steps in the code, as this is a major indicator of AI-generated code. 3. Avoid highly verbose AI structures; do not modularize small helper logic into separate functions unless it is complex. 4. Write standard, mathematically correct algorithms (e.g., standard binary search pointer updates and boundaries, correct bit manipulation loops). Do NOT write buggy or overly complex non-textbook variations just to look different. 5. Include small, natural defensive/boundary checks (e.g., 'if not arr: return 0') to mimic hand-written student code. 6. STRICT FORMATTING: Choose exactly ONE structure format per the following rules: {env_instruction}",
  "explanation": "Provide a clean, concise explanation of the optimal approach in plain, intuitive English. Explicitly address how the solution satisfies any user-specified constraints/requirements (e.g. O(N) time, O(1) space, no built-in sort).",
  "complexity": {{ "time": "O(...)", "space": "O(...)" }},
  "driverCode": "Write the COMPLETE, EXECUTABLE code in {language} (including all imports/includes, the solutionCode, and a main execution block). The main block MUST run a comprehensive set of test cases (normal, boundary, edge, and stress cases). For each test case, execute the solution, compare actual vs expected, and build a JSON array of the results. The script MUST output the exact string '---TEST_RESULTS_JSON---' followed by the valid JSON array of objects: [{{\\"passed\\": true/false, \\"actual\\": \\"...\\", \\"expected\\": \\"...\\", \\"inputs\\": [...]}}]. Ensure the code catches exceptions. Do NOT print anything else to stdout."
}}
{completion_instruction}
{error_fix_instruction}
IMPORTANT: Output ONLY valid JSON.
"""

@router.post("/extract-text")
async def extract_text(req: ExtractTextRequest):
    import asyncio
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set.")

    def _call_gemini_vision():
        # remove data:image/png;base64, prefix if present
        b64 = req.image_base64
        if "," in b64:
            b64 = b64.split(",")[1]
        
        image_bytes = base64.b64decode(b64)

        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg",
                    ),
                    "Extract all the text from this image exactly as written, but format it cleanly using GitHub Flavored Markdown. Use proper headers (e.g. ## Example 1), bullet points for constraints, bold text for labels (e.g. **Input:**), and backticks for code snippets. You MUST preserve all line breaks, mathematical formulas, and visual structure perfectly. Return ONLY the Markdown text, no conversational filler."
                ]
            )
            return response.text
        except Exception as e:
            print(f"Gemini vision failed: {e}. Falling back to Groq Llama 3.2 90B Vision...")
        
        try:
            from groq import Groq
            groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
            groq_response = groq_client.chat.completions.create(
                model="llama-3.2-90b-vision-preview",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all the text from this image exactly as written, but format it cleanly using GitHub Flavored Markdown. Use proper headers (e.g. ## Example 1), bullet points for constraints, bold text for labels (e.g. **Input:**), and backticks for code snippets. You MUST preserve all line breaks, mathematical formulas, and visual structure perfectly. Return ONLY the Markdown text, no conversational filler."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                    ]
                }]
            )
            return groq_response.choices[0].message.content
        except Exception as groq_err:
            print(f"Groq vision fallback failed: {groq_err}. Falling back to OpenRouter free tier...")
            import openai
            openai_client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.environ.get("OPENROUTER_API_KEY", ""),
            )
            free_vision_models = [
                "nvidia/nemotron-nano-12b-v2-vl:free",
                "openrouter/free"
            ]
            last_openrouter_err = None
            for fallback_model in free_vision_models:
                try:
                    print(f"Trying OpenRouter free vision model: {fallback_model}...")
                    openrouter_response = openai_client.chat.completions.create(
                        model=fallback_model,
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Extract all the text from this image exactly as written, but format it cleanly using GitHub Flavored Markdown. Use proper headers (e.g. ## Example 1), bullet points for constraints, bold text for labels (e.g. **Input:**), and backticks for code snippets. You MUST preserve all line breaks, mathematical formulas, and visual structure perfectly. Return ONLY the Markdown text, no conversational filler."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                            ]
                        }]
                    )
                    return openrouter_response.choices[0].message.content
                except Exception as openrouter_err:
                    last_openrouter_err = openrouter_err
                    print(f"OpenRouter {fallback_model} failed: {openrouter_err}")
                    continue
            raise last_openrouter_err

    try:
        text = await asyncio.to_thread(_call_gemini_vision)
        return {"extracted_text": text}
    except Exception as e:
        print(f"OCR Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

async def execute_on_piston(code: str, language: str) -> list:
    PISTON_LANGUAGES = {
        "python": "python",
        "cpp": "c++",
        "java": "java",
        "javascript": "javascript"
    }
    PISTON_VERSIONS = {
        "python": "3.10.0",
        "cpp": "10.2.0",
        "java": "15.0.2",
        "javascript": "16.3.0"
    }
    
    lang = PISTON_LANGUAGES.get(language, "python")
    version = PISTON_VERSIONS.get(language, "3.10.0")

    payload = {
        "language": lang,
        "version": version,
        "files": [{"content": code}],
        "compile_timeout": 10000,
        "run_timeout": 10000
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("https://emkc.org/api/v2/piston/execute", json=payload, timeout=25.0)
            if response.status_code != 200:
                print(f"Piston API Error: {response.status_code} {response.text}")
                return []
            
            data = response.json()
            run_output = data.get("run", {}).get("output", "")
            
            if "---TEST_RESULTS_JSON---" in run_output:
                json_str = run_output.split("---TEST_RESULTS_JSON---")[-1].strip()
                try:
                    return json.loads(json_str)
                except Exception as e:
                    print(f"JSON Parse Error from Piston: {e}, Output: {run_output}")
            return []
    except Exception as e:
        print(f"Piston execution exception: {e}")
        return []

@router.post("/analyze")
async def analyze_practice(req: PracticeRequest):
    
    user_msg = f"Problem Statement:\n{req.problem}\n\n"
    if req.constraints:
        user_msg += f"Constraints:\n{req.constraints}\n\n"
    if req.userAttempt:
        user_msg += f"My Attempt (Code containing error):\n{req.userAttempt}\n\n" if req.errorMessage else f"My Attempt:\n{req.userAttempt}\n\n"
    if req.errorMessage:
        user_msg += f"Execution Error / Runtime Error / Compilation Error:\n{req.errorMessage}\n\n"
        
    try:
        # Step 1: Generate analysis and code via Gemini
        system_prompt = build_system_prompt(
            req.language, 
            req.environment, 
            req.verbosity, 
            req.isCompletionMode, 
            req.starterCode, 
            req.completionOutputFormat,
            is_error_fix=bool(req.errorMessage)
        )
        analysis = await ask_gemini_json(system_prompt, user_msg, req.model)
        
        # Aggressively strip comments from solution code
        if "solutionCode" in analysis:
            raw_code = analysis["solutionCode"]
            cleaned_lines = []
            for line in raw_code.splitlines():
                if line.strip().startswith("#") or line.strip().startswith("//"):
                    continue
                cleaned_lines.append(line)
            analysis["solutionCode"] = "\n".join(cleaned_lines)
            
        # Step 2: Verify code via Judge0 (if enabled)
        driver_code = analysis.get("driverCode", "")
        verification_results = []
        if driver_code and req.verify_code:
            try:
                res = await execute_on_judge0(driver_code, req.language)
                stdout = res.get("stdout", "")
                parsed_results, _ = parse_driver_results(stdout)
                
                if parsed_results is not None:
                    verification_results = parsed_results
                else:
                    verification_results = [{"passed": False, "error": "Failed to parse driver results.", "stdout": stdout}]
            except Exception as e:
                verification_results = [{"passed": False, "error": f"Execution failed: {str(e)}"}]
                
        analysis["verification"] = verification_results
            
        # Step 3: Log to Supabase
        if supabase:
            try:
                # Basic topic extraction logic (could be improved with LLM)
                topic = "general"
                problem_lower = req.problem.lower()
                if "array" in problem_lower: topic = "arrays"
                elif "string" in problem_lower: topic = "strings"
                elif "tree" in problem_lower: topic = "trees"
                elif "graph" in problem_lower: topic = "graphs"
                elif "dynamic programming" in problem_lower or "dp" in problem_lower.split(): topic = "dp"
                
                passed_all = all(tc.get("passed", False) for tc in verification_results) if verification_results else False
                
                supabase.table("practice_attempts").insert({
                    "problem_text": req.problem,
                    "language": req.language,
                    "topic": topic,
                    "user_code": req.userAttempt,
                    "generated_code": analysis.get("solutionCode", ""),
                    "passed_normal": passed_all,
                    "passed_boundary": passed_all,
                    "passed_edge": passed_all,
                    "passed_stress": passed_all,
                    "complexity_time": analysis.get("complexity", {}).get("time", ""),
                    "complexity_space": analysis.get("complexity", {}).get("space", ""),
                    "attempted_first": req.attemptedFirst
                }).execute()
            except Exception as e:
                print(f"Supabase logging failed: {e}")
                
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
