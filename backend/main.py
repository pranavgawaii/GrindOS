from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from pathlib import Path
from llm_router import ask_llm
from pydantic import BaseModel
import httpx
import base64
import re
from judge0_router import router as judge0_router

app = FastAPI()

app.include_router(judge0_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8080",
        # Add your production domain here e.g. "https://grindos.in"
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

_PROFILE_PATH = Path(__file__).parent / "pranav_profile.json"
with open(_PROFILE_PATH, encoding="utf-8") as f:
    PRANAV = json.load(f)

class AskRequest(BaseModel):
    question: str
    mode: str = "general"

class MockRequest(BaseModel):
    subject: str
    question: str
    user_answer: str

class ScriptRequest(BaseModel):
    scenario: str

# Build system prompt based on mode
def build_system_prompt(mode: str) -> str:
    return f"""You are an elite campus placement preparation copilot and personal AI assistant representing Pranav Gawai.
    Here is Pranav's complete professional profile:
    {json.dumps(PRANAV, indent=2)}

    Your core instructions are:
    1. PERSONAL & HR INQUIRIES: When asked about Pranav's career, strengths, weakness, achievements, or project details, ALWAYS respond in the FIRST PERSON as Pranav Gawai. Be direct, authentic, confident, and back up claims with metrics and specific projects. Keep answers under 150 words unless explicitly asked to expand.
    2. TECHNICAL CS TOPICS: When asked about a technical CS concept (in Operating Systems, DBMS, Networks, OOPS, or DSA) or GATE exam topics, act as a strict but helpful placement mentor. Provide:
       - A clear, concise 1-sentence definition.
       - A memorable, real-world analogy or example.
       - Interview talking points (exact words Pranav should say to stand out in an interview).
       - If explaining a process flow, architecture relationship, database schema layout, comparison (e.g., composition vs inheritance), or lifecycle, you MUST include a neat, valid Mermaid flowchart block in your answer using:
         ```mermaid
         (mermaid graph syntax here)
         ```
    3. PROJECT DEEP-DIVES: Be ready to explain the architecture, tech choices, trade-offs, and scaling decisions for Pranav's projects (like PlacePro or Mnemo).
    4. GENERAL & GATE PREP: Give mathematically precise, campus-focused advice for aptitude, core subjects, and GATE questions.
    """

@app.post("/ask")
async def ask(req: AskRequest):
    try:
        system = build_system_prompt(req.mode)
        answer = await ask_llm(system, req.question)
        return {"answer": answer, "mode": req.mode}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")

@app.post("/mock-interview")
async def mock_interview(req: MockRequest):
    system = f"""You are a strict technical interviewer.
    Grade this answer honestly out of 10.
    
    Question: {req.question}
    Subject: {req.subject}
    
    Respond in this EXACT JSON format:
    {{
      "score": 7,
      "correct_points": ["point 1", "point 2"],
      "missing_points": ["missing 1", "missing 2"],
      "model_answer": "The ideal answer in 4-6 sentences."
    }}"""
    try:
        result = await ask_llm(system, req.user_answer)
        try:
            parsed = json.loads(result)
            return parsed
        except json.JSONDecodeError:
            return {"score": 0, "correct_points": [], 
                    "missing_points": ["Could not parse AI response — try again"], 
                    "model_answer": result}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")

@app.post("/generate-script")
async def generate_script(req: ScriptRequest):
    system = build_system_prompt("hr")
    prompt = f"""Generate a complete interview script 
    for this scenario: {req.scenario}
    
    Include:
    1. Complete answer (word for word what to say)
    2. Key points to definitely mention
    3. What NOT to say
    4. Estimated speaking time in seconds
    
    Format as JSON:
    {{
      "script": "complete answer here",
      "key_points": ["point 1", "point 2"],
      "avoid": ["avoid 1", "avoid 2"],
      "duration_seconds": 45
    }}"""
    
    result = await ask_llm(system, prompt)
    try:
        return json.loads(result)
    except:
        return {"script": result, "key_points": [], 
                "avoid": [], "duration_seconds": 60}

@app.get("/last-minute/{subject}")
async def last_minute(subject: str):
    prompt = f"""Give me a last-minute revision guide 
    for {subject} for a campus placement interview.
    
    Respond as JSON:
    {{
      "subject": "{subject}",
      "must_know": ["concept 1", "concept 2", ...5 items],
      "one_liners": ["explanation 1", ...5 items],
      "top_questions": ["question 1", ...5 items],
      "model_answers": ["answer 1", ...5 items]
    }}"""
    
    result = await ask_llm(
        "You are a placement prep expert.", 
        prompt
    )
    try:
        return json.loads(result)
    except:
        return {"subject": subject, "content": result}

@app.get("/health")
def health():
    return {"status": "ok", "message": "GrindOS AI backend running"}
