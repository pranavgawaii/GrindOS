import os
from pathlib import Path
from dotenv import load_dotenv

# Explicitly load .env from the same directory as this file
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

async def ask_llm(system_prompt: str, user_message: str) -> str:
    """Try Gemini → Groq → OpenRouter in order. Return first successful response."""

    # 1. Gemini 2.5 Flash — new google-genai SDK
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7,
            ),
        )
        print("✅ Model used: Gemini 2.5 Flash")
        return response.text
    except Exception as e:
        print(f"❌ Gemini failed: {e}")

    # 2. Groq Llama 3.3 70B
    try:
        from groq import AsyncGroq
        groq_client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY", ""))
        response = await groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        print("✅ Model used: Groq Llama 3.3 70B")
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Groq failed: {e}")

    # 3. OpenRouter Llama 3.3 70B
    try:
        from openai import AsyncOpenAI
        openai_client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY", ""),
        )
        response = await openai_client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        print("✅ Model used: OpenRouter Llama 3.3 70B")
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ OpenRouter failed: {e}")

    raise Exception("All LLMs unavailable")
