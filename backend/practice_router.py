import json
import os
import re
import base64
import re
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
    attemptedFirst: bool
    environment: str = "leetcode"
    verbosity: str = "detailed"

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

async def ask_gemini_json(system_prompt: str, user_message: str) -> dict:
    import asyncio
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set.")

    def _call_gemini():
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

    try:
        content = await asyncio.to_thread(_call_gemini)
        # Ensure we strip any markdown blocks if the LLM adds them despite response_mime_type
        content = re.sub(r"^```json\s*", "", content, flags=re.IGNORECASE|re.MULTILINE)
        content = re.sub(r"^```\s*", "", content, flags=re.MULTILINE)
        return json.loads(content.strip())
    except Exception as e:
        print(f"Gemini JSON Error: {e}")
        raise Exception(f"Failed to generate analysis: {str(e)}")

def build_system_prompt(language: str, environment: str, verbosity: str) -> str:
    env_instruction = ""
    if environment == "leetcode":
        env_instruction = "Provide ONLY the class/function definition (LeetCode style)."
    else:
        env_instruction = "Provide a FULL script that parses input from sys.stdin and prints to stdout (OA style)."

    concise_instruction = ""
    if verbosity == "concise":
        concise_instruction = "Since the user requested CONCISE mode, leave `naiveApproach`, `pseudocode`, `comparisonTable`, and `rederivePrompt` as empty strings or empty arrays."

    return f"""You are an elite competitive programming coach and AI software engineer. 
The user will provide a DSA problem, their target language ({language}), and optionally their attempt.

You must return a raw JSON object with EXACTLY the following structure:
{{
  "constraintsCheck": "Briefly analyze the required time/space complexity based on typical constraints.",
  "naiveApproach": "Explain the brute force approach and why it's too slow.",
  "optimizedApproach": "Explain the optimal approach in plain, intuitive English.",
  "pseudocode": "Write high-level pseudocode for the optimal approach.",
  "solutionCode": "Write the final optimal code in {language}. Use natural, human-readable variable names. No docstrings, minimal comments. {env_instruction}",
  "driverCode": "Write the COMPLETE, EXECUTABLE code in {language} (including all imports/includes, the solutionCode, and a main execution block). The main block MUST run a comprehensive set of test cases (normal, boundary, edge, and stress cases). For each test case, execute the solution, compare actual vs expected, and build a JSON array of the results. The script MUST output the exact string '---TEST_RESULTS_JSON---' followed by the valid JSON array of objects: [{{\"passed\": true/false, \"actual\": \"...\", \"expected\": \"...\", \"inputs\": [...]}}]. Ensure the code catches exceptions. Do NOT print anything else to stdout.",
  "complexity": {{ "time": "O(...)", "space": "O(...)" }},
  "comparisonTable": [ {{"feature": "...", "humanStyle": "...", "aiStyle": "..."}} ],
  "feedback": "Actionable feedback on the user's attempt (if provided), or a tip on what to learn.",
  "rederivePrompt": "A short prompt the user can read to try re-deriving the solution themselves."
}}
{concise_instruction}
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
        client = genai.Client(api_key=api_key)
        # remove data:image/png;base64, prefix if present
        b64 = req.image_base64
        if "," in b64:
            b64 = b64.split(",")[1]
        
        image_bytes = base64.b64decode(b64)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg",
                ),
                "Extract all the text from this image exactly as written. Preserve formatting, mathematical formulas, constraints, and code snippets. Return ONLY the extracted text, no conversational filler."
            ]
        )
        return response.text

    try:
        text = await asyncio.to_thread(_call_gemini_vision)
        return {"extracted_text": text}
    except Exception as e:
        print(f"OCR Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

@router.post("/analyze")
async def analyze_practice(req: PracticeRequest):
    system_prompt = build_system_prompt(req.language, req.environment, req.verbosity)
    
    user_msg = f"Problem Statement:\n{req.problem}\n\n"
    if req.constraints:
        user_msg += f"Constraints:\n{req.constraints}\n\n"
    if req.userAttempt:
        user_msg += f"My Attempt:\n{req.userAttempt}\n\n"
        
    try:
        # Step 1: Generate analysis and code via Gemini
        analysis = await ask_gemini_json(system_prompt, user_msg)
        
        # Step 2: Verify code via Judge0
        driver_code = analysis.get("driverCode", "")
        verification_results = []
        if driver_code:
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
        
        # Categorize test cases into normal/boundary/edge/stress based on index or just pass them raw
        # For simplicity, we'll just pass the raw verification array to the frontend
        analysis["verification"] = verification_results
        
        # We don't need to send driverCode back to frontend
        if "driverCode" in analysis:
            del analysis["driverCode"]
            
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
