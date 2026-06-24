import json
import os
import re
import base64
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
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
    namingStyle: str = "short"

class ComplexityInfo(BaseModel):
    time: str = Field(..., description="Time complexity of the solution, e.g. O(N) or O(log N).")
    space: str = Field(..., description="Space complexity of the solution, e.g. O(1) or O(N).")

class ComparisonRow(BaseModel):
    feature: str = Field(..., description="The coding aspect compared.")
    aiStyle: str = Field(..., description="Standard AI generation style.")
    humanStyle: str = Field(..., description="Human student under pressure style.")

class AnalysisResponse(BaseModel):
    solutionCode: str = Field(
        ...,
        description=(
            "The final optimal implementation code in the target programming language. "
            "CRITICAL PLAGIARISM-BYPASS & HUMANIZATION RULES: "
            "1. NO canonical/textbook-first loops or structures for famous problems. "
            "For Reverse Bits: DO NOT write any loop (for/while). In Python, use: "
            "`import sys, json; raw = sys.stdin.read().strip(); "
            "try: data = json.loads(raw); n = data['n'] if isinstance(data, dict) else data; "
            "except: n = int(raw); ans = int(f'{n:032b}'[::-1], 2); print(ans)` or divide-and-conquer mask swaps. "
            "2. NO COMMENTS of any kind (inline or block). NO docstrings. NO type hints. "
            "3. Parse stdin robustly: if input is JSON (starts with { or [), parse it via json.loads. "
            "4. Choose exactly one format per environment rules (flat OA script vs LeetCode class)."
        )
    )
    explanation: str = Field(..., description="Concise English explanation of the approach.")
    complexity: ComplexityInfo = Field(..., description="Time and space complexity of the solution.")
    driverCode: str = Field(..., description="Executable unit-test driver code wrapper.")
    constraintsCheck: Optional[str] = Field(None, description="Check of problem constraints.")
    naiveApproach: Optional[str] = Field(None, description="Naive algorithm description.")
    optimizedApproach: Optional[str] = Field(None, description="Optimized algorithm description.")
    pseudocode: Optional[str] = Field(None, description="Pseudocode for the algorithm.")
    comparisonTable: Optional[List[ComparisonRow]] = Field(None, description="AI vs human code comparison table.")
    feedback: Optional[str] = Field(None, description="General student feedback.")
    rederivePrompt: Optional[str] = Field(None, description="Rederivation prompts.")

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
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")

    def _validate_and_dump(content_str: str) -> dict:
        clean_content = re.sub(r"^```json\s*", "", content_str, flags=re.IGNORECASE|re.MULTILINE)
        clean_content = re.sub(r"^```\s*", "", clean_content, flags=re.MULTILINE)
        parsed = json.loads(clean_content.strip())
        validated = AnalysisResponse.model_validate(parsed)
        return validated.model_dump()

    def _call_llm():
        # 1. Claude/Anthropic blocks
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
                    try:
                        return _validate_and_dump(response.content[0].text)
                    except Exception as parse_err:
                        print(f"Anthropic Claude parsing failed: {parse_err}")
                except Exception as e:
                    print(f"Anthropic Claude API failed: {e}. Trying OpenRouter Claude...")
            
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
                        response_format={"type": "json_object"},
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ]
                    )
                    try:
                        return _validate_and_dump(response.choices[0].message.content)
                    except Exception as parse_err:
                        print(f"OpenRouter Claude parsing failed: {parse_err}")
                except Exception as e:
                    print(f"OpenRouter Claude fallback failed: {e}. Falling back to default Gemini/Llama pipeline...")

        # 2. Primary Gemini call via google-genai response_schema
        if api_key:
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=user_message,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.2,
                        response_mime_type="application/json",
                        response_schema=AnalysisResponse
                    ),
                )
                try:
                    return _validate_and_dump(response.text)
                except Exception as parse_err:
                    print(f"Gemini response parsing failed: {parse_err}")
            except Exception as e:
                print(f"Gemini failed in analysis: {e}. Falling back to OpenRouter Gemini 2.5 Flash...")

        # 3. Fallback to OpenRouter Gemini 2.5 Flash (Paid, extremely cheap/reliable, using credits)
        if openrouter_key:
            try:
                import openai
                client = openai.OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=openrouter_key,
                )
                response = client.chat.completions.create(
                    model="google/gemini-2.5-flash",
                    max_tokens=2000,
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ]
                )
                try:
                    return _validate_and_dump(response.choices[0].message.content)
                except Exception as parse_err:
                    print(f"OpenRouter Gemini 2.5 Flash parsing failed: {parse_err}. Trying Groq Llama...")
            except Exception as e:
                print(f"OpenRouter Gemini 2.5 Flash failed: {e}. Trying Groq Llama...")

        # 4. Fallback to Groq Llama 3.3 70B
        try:
            from groq import Groq
            groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
            groq_response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            try:
                return _validate_and_dump(groq_response.choices[0].message.content)
            except Exception as parse_err:
                print(f"Groq parsing failed: {parse_err}. Trying OpenRouter free models...")
        except Exception as groq_err:
            print(f"Groq fallback failed: {groq_err}. Falling back to OpenRouter free tier...")

        # 5. Fallback to OpenRouter free models
        if openrouter_key:
            import openai
            openai_client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=openrouter_key,
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
                        max_tokens=2000,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ]
                    )
                    try:
                        return _validate_and_dump(openrouter_response.choices[0].message.content)
                    except Exception as parse_err:
                        print(f"OpenRouter free model {fallback_model} parsing failed: {parse_err}")
                        last_openrouter_err = parse_err
                except Exception as openrouter_err:
                    last_openrouter_err = openrouter_err
                    print(f"OpenRouter {fallback_model} failed: {openrouter_err}")
                    continue
            raise last_openrouter_err
        else:
            raise Exception("No active LLM providers or fallbacks succeeded.")

    try:
        content = await asyncio.to_thread(_call_llm)
        return content
    except Exception as e:
        raise Exception(f"Failed to generate analysis: {str(e)}")

def build_system_prompt(language: str, environment: str, verbosity: str, is_completion: bool = False, starter_code: str = "", output_format: str = "snippet", is_error_fix: bool = False, naming_style: str = "short") -> str:
    env_instruction = ""
    if environment == "leetcode":
        env_instruction = (
            "Provide ONLY the class/function definition (LeetCode style). Do NOT include sys.stdin or __main__. "
            "CRITICAL CODESIGNAL/FUNCTION-BASED COMPATIBILITY: "
            "Always include both a standard class Solution (LeetCode style) AND a flat alias function at the bottom "
            "matching the problem name or named 'solution' (CodeSignal style) that instantiates the class and calls it, "
            "so the code works out-of-the-box on both LeetCode and CodeSignal without editing. "
            "For example: \n"
            "class Solution:\n"
            "    def reverseBits(self, n: int) -> int:\n"
            "        return int(f'{n:032b}'[::-1], 2)\n\n"
            "def solution(n):\n"
            "    return Solution().reverseBits(n)"
        )
    elif environment == "oa":
        env_instruction = (
            'Provide a pure sys.stdin/stdout script (OA style). Do NOT use "class Solution". '
            'Do NOT wrap the logic in ANY functions (like "def main()" or "def solve()"). '
            'Do NOT use "if __name__ == \'__main__\':". Write the sys.stdin parsing and solution logic completely flat at the root level. '
            'CRITICAL: You MUST parse stdin dynamically to handle BOTH raw inputs (e.g. "12345") and JSON inputs (e.g. "{\"n\": 12345}" or "{\"nums\": [...]}"). '
            'If the input starts with "{" or "[", parse it with JSON and extract the parameter value (e.g. data["n"] or data["nums"]). Fallback to raw parsing if not JSON.'
        )
    else:
        # Default/Auto format selection per SKILL.md guidelines
        env_instruction = (
            'Automatically select the code structure format based on the problem statement context. '
            '1. If the problem statement explicitly mentions standard input, stdin, or reading lines/input (e.g. "Read from stdin", "Print the output", "The first line contains"), then write a flat sys.stdin/stdout script (OA style) at the root level without "class Solution" or any wrapping functions. In this case, you MUST parse stdin dynamically to handle BOTH raw inputs and JSON inputs (e.g., "{\"n\": 12345}"). '
            '2. Otherwise, write a class/function template (LeetCode style) wrapped in a Solution class or standard function signature. '
            'Always include both a standard class Solution (LeetCode style) AND a flat alias function at the bottom '
            "matching the problem name or named 'solution' (CodeSignal style) that instantiates the class and calls it, "
            "so the code works out-of-the-box on both LeetCode and CodeSignal without editing. "
            'DO NOT mix both styles. Choose exactly one.'
        )

    naming_style_instruction = ""
    if naming_style == "descriptive":
        naming_style_instruction = (
            "4. DESCRIPTIVE NAMING PERSONA:\n"
            "   You MUST use highly descriptive and meaningful variable and function/method names. "
            "For example: use `studentDataIterator` instead of `i` or `idx`, `matchingIndexTracker` instead of `match` or `k`, "
            "`targetSumDifference` instead of `diff`, `trappedWaterSum` instead of `ans` or `res`, "
            "`leftBoundaryPointer` instead of `l` or `left`, and `rightBoundaryPointer` instead of `r` or `right`. "
            "Every variable, loop counter, tracker, and parameter must have a long, readable, meaningful name. "
            "Strictly AVOID short, cryptic competitive programming names (like `n`, `m`, `i`, `j`, `seen`, `dp`, `ans`, `res`)."
        )
    else:
        naming_style_instruction = (
            "4. CONSISTENT STUDENT PERSONA:\n"
            "   The code must look like it was written by a real, competent student under time pressure. "
            "Use short, standard variable names (e.g., 'n', 'm', 'i', 'j', 'l', 'r', 'seen', 'dp'). "
            "Pick one consistent variable name for result (e.g. 'ans' or 'res') and stick with it."
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

    prompt = """You are an elite competitive programming coach and AI software engineer executing in Online Assessment (OA) stealth mode. 
The user will provide a DSA problem, their target language ({language}), optionally user constraints/requirements, and optionally their attempt.

## CRITICAL RULES FOR GENERATING THE SOLUTION CODE
1. FAMOUS-PROBLEM VARIATION & PLAGIARISM-BYPASS:
   For famous, commonly repeated DSA problems (like Two Sum, Reverse Bits, contains duplicates, Trapping Rain Water, etc.), you MUST NOT write the canonical textbook first solution. Instead, deliberately write an alternative correct, optimal, but structurally distinct variant to bypass plagiarism checkers (like MOSS/Turnitin) and keep it stealthy.
   * Reverse Bits (Python): DO NOT write any loop (for/while) or standard iteration. Write it in a single line using binary formatting and string slicing, e.g.:
     `import sys, json; raw = sys.stdin.read().strip(); try: data = json.loads(raw); n = data['n'] if isinstance(data, dict) else data; except: n = int(raw); ans = int(f"{n:032b}"[::-1], 2); print(ans)` or a bitwise divide-and-conquer mask swap approach.
   * Two Sum (Python): DO NOT use the standard single-pass hash map returning indices. Sort pairs of (value, index) and use a two-pointer approach, or loop and check in a slightly restructured manner.
   * Contains Duplicate: DO NOT use `len(nums) != len(set(nums))`. Sort and run a single-pass adjacent comparison, or use a custom hash set loop with an early exit.
2. NO COMMENTS OF ANY KIND:
   The output code must be 100% comment-free and clean. Strictly NO comments of any kind (neither inline comments starting with '#'/'//', nor separate block comments, nor docstrings, nor type hints).
3. ROBUST STDIN INPUT PARSING FOR FLAT SCRIPTS (OA STYLE):
   If writing a flat script reading from stdin, you MUST parse stdin dynamically to handle BOTH raw inputs (e.g. "12345") and JSON inputs (e.g. '{"n": 12345}' or '{"nums": [...]}').
   Check if the input starts with "{" or "[" and parse it using `json.loads` if so, extracting the parameter value. Fallback to raw parsing if not JSON.
{naming_style_instruction}
5. PURE ENVIRONMENT FORMATTING:
   Choose exactly ONE format: {env_instruction}

## OUTPUT FORMAT
You must return a raw JSON object with EXACTLY the following structure. ENSURE ALL CODE STRINGS ARE PROPERLY ESCAPED FOR JSON (e.g., escape double quotes as \" and newlines as \n):
{
  "solutionCode": "The final optimal implementation code in {language} (comment-free, humanized, plagiarism-bypassed, and matching the environment format).",
  "explanation": "Provide a clean, concise explanation of the optimal approach in plain, intuitive English. Explicitly address how the solution satisfies any user-specified constraints/requirements (e.g. O(N) time, O(1) space, no built-in sort).",
  "complexity": { "time": "O(...)", "space": "O(...)" },
  "driverCode": "Write the COMPLETE, EXECUTABLE code in {language} (including all imports/includes, a test runner, and a main execution block). The main block MUST run a comprehensive set of test cases (normal, boundary, edge, and stress cases). For each test case, execute the solution, compare actual vs expected, and build a JSON array of the results. The script MUST output the exact string '---TEST_RESULTS_JSON---' followed by the valid JSON array of objects: [{\"passed\": true/false, \"actual\": \"...\", \"expected\": \"...\", \"inputs\": [...]}]. Ensure the code catches exceptions. Do NOT print anything else to stdout.\\nCRITICAL DRIVER RULES:\\n1. For Python, be extremely careful with string quotes when specifying mock inputs: if a mock input contains double quotes like '{\"n\": 1}', use single quotes around the outer string like '{\"n\": 1}' or properly escape them to avoid syntax errors.\\n2. The solutionCode itself MUST remain completely flat. Inside the driverCode, wrap the flat solution logic inside a solver function/method.\\n3. You MUST include all standard imports/headers required by both the solution and the driver (e.g. in Python: import sys, json, math, heapq, collections; in C++: #include <iostream>, <vector>, <unordered_map>, <unordered_set>, <queue>, <stack>, <algorithm>, <string>, <sstream>; in Java: import java.util.*, java.io.*).\\n4. DATA STRUCTURE DEFINITIONS: If the problem uses common custom structures, you MUST define them at the top of the driverCode:\\n   - Linked Lists: Define `class ListNode` (for singly linked lists) or `class Node` (for doubly linked lists or random pointer lists) with proper constructors.\\n   - Binary Trees / BST: Define `class TreeNode` (with val, left, right).\\n   - N-ary Trees / Graphs: Define `class Node` (with val, children, neighbors, etc. as appropriate for the problem type).\\n5. HELPER FUNCTIONS: For custom structures, you MUST write robust helper functions in the driverCode to construct them from array representations (e.g. level-order build_tree for binary trees handling nulls, build_list for linked lists) and serialize them back to basic serializable types (like list or dict) before printing the test results JSON. Never output a raw object memory address as 'actual' or 'expected'."
}
{completion_instruction}
{error_fix_instruction}
IMPORTANT: Output ONLY valid JSON.
"""
    return (
        prompt
        .replace("{language}", language)
        .replace("{env_instruction}", env_instruction)
        .replace("{completion_instruction}", completion_instruction)
        .replace("{error_fix_instruction}", error_fix_instruction)
        .replace("{naming_style_instruction}", naming_style_instruction)
    )

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
                model="gemini-2.5-flash-lite",
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
            is_error_fix=bool(req.errorMessage),
            naming_style=req.namingStyle
        )
        analysis = await ask_gemini_json(system_prompt, user_msg, req.model)
        
        # Self-correction loop to validate constraints and syntax before proceeding
        attempts = 0
        while attempts < 3:
            solution = analysis.get("solutionCode", "")
            driver_code = analysis.get("driverCode", "")
            error_reasons = []
            
            # Check 1: Famous problems - Reverse Bits must not use loops in Python
            is_reverse_bits = "reverse" in req.problem.lower() and "bit" in req.problem.lower()
            if is_reverse_bits and req.language.lower() in ("python", "py"):
                if "for " in solution or "while " in solution:
                    error_reasons.append("For Reverse Bits in Python, you MUST NOT use any loop (for/while). Write it in a single line using binary formatting and string slicing, e.g. `ans = int(f'{n:032b}'[::-1], 2)`.")
            
            # Check 2: Python driverCode syntax validation
            if req.language.lower() in ("python", "py") and driver_code:
                try:
                    compile(driver_code, "<string>", "exec")
                except SyntaxError as syntax_err:
                    error_reasons.append(f"The generated driverCode has a Python SyntaxError: {syntax_err}. Ensure all string quotes and newlines in test cases are properly escaped (e.g. do not put raw unescaped newlines inside single-quoted strings).")
            
            # Check 3: Naming style validation if descriptive is requested
            if req.namingStyle == "descriptive":
                short_vars = ["i", "j", "n", "m", "dp", "ans", "res"]
                detected_short = []
                for var in short_vars:
                    if re.search(r'\b' + var + r'\b', solution):
                        detected_short.append(f"`{var}`")
                if detected_short:
                    error_reasons.append(
                        f"You chose the DESCRIPTIVE naming style, but the code still uses short variables: {', '.join(detected_short)}. "
                        "You MUST rewrite these to be descriptive (e.g. elementIndex, targetSumDifference, totalWaterVolume, arrayLength)."
                    )
            
            if not error_reasons:
                break
                
            attempts += 1
            feedback_msg = "Your previous response violated critical requirements:\n" + "\n".join(f"- {err}" for err in error_reasons) + "\n\nPlease rewrite the JSON response to correct these issues. Ensure all syntax is valid and constraints are strictly met."
            print(f"Self-correcting attempt {attempts} for practice router...")
            analysis = await ask_gemini_json(system_prompt + f"\n\nCRITICAL SYSTEM FEEDBACK (ATTEMPT {attempts}):\n{feedback_msg}", user_msg, req.model)
        
        # Aggressively strip comments from solution code
        if "solutionCode" in analysis:
            raw_code = analysis["solutionCode"]
            cleaned_lines = []
            lang_lower = req.language.lower()
            for line in raw_code.splitlines():
                trimmed = line.strip()
                if lang_lower in ("python", "py"):
                    if trimmed.startswith("#"):
                        continue
                    if "#" in line:
                        if '"' not in line and "'" not in line:
                            line = line.split("#", 1)[0]
                        elif " #" in line or "\t#" in line or "  #" in line:
                            line = line.split(" #", 1)[0] if " #" in line else line.split("\t#", 1)[0] if "\t#" in line else line.split("  #", 1)[0]
                    cleaned_lines.append(line.rstrip())
                else:  # c++, java, javascript
                    if trimmed.startswith("//") or trimmed.startswith("/*"):
                        continue
                    if "//" in line:
                        if '"' not in line and "'" not in line:
                            line = line.split("//", 1)[0]
                        elif " //" in line or "\t//" in line or "  //" in line:
                            line = line.split(" //", 1)[0] if " //" in line else line.split("\t//", 1)[0] if "\t//" in line else line.split("  //", 1)[0]
                    cleaned_lines.append(line.rstrip())
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

@router.get("/document/{document_name}")
async def get_document_url(document_name: str):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    try:
        # Create a signed URL that expires in 120 seconds for reading
        res = supabase.storage.from_("grindos-documents").create_signed_url(document_name, 120)
        url = res.get("signedURL") if isinstance(res, dict) else str(res)
        if not url:
            raise Exception("Could not generate URL from Supabase response")
        return {"url": url}
    except Exception as e:
        print(f"Failed to generate signed URL for {document_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
