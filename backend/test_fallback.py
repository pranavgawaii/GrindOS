import os
import openai
from dotenv import load_dotenv

load_dotenv()

print("Testing OpenRouter Fallback Models...")
openai_client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY", ""),
)

free_models = [
    "google/gemini-2.0-flash-lite-preview-02-05:free",
    "google/gemini-2.0-flash-exp:free",
    "mistralai/mistral-nemo:free",
    "meta-llama/llama-3.3-70b-instruct:free"
]

success = False
for fallback_model in free_models:
    try:
        print(f"\\n--- Trying {fallback_model} ---")
        response = openai_client.chat.completions.create(
            model=fallback_model,
            messages=[
                {"role": "system", "content": "You are a testing bot. Output a JSON object with a single key 'status' set to 'ok'."},
                {"role": "user", "content": "Test"}
            ]
        )
        print("✅ SUCCESS!")
        print("Response:", response.choices[0].message.content)
        success = True
        break
    except Exception as e:
        print(f"❌ FAILED: {e}")

if success:
    print("\\n🎉 Cascading fallback test PASSED! At least one free model is completely operational.")
else:
    print("\\n🚨 Cascading fallback test FAILED! All free models returned an error.")
