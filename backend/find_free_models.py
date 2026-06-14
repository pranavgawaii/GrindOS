import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY", "")

try:
    response = requests.get("https://openrouter.ai/api/v1/models", headers={"Authorization": f"Bearer {api_key}"})
    models = response.json().get("data", [])

    free_models = []
    for model in models:
        pricing = model.get("pricing", {})
        if "free" in model["id"].lower() or (pricing.get("prompt", "-1") == "0" and pricing.get("completion", "-1") == "0"):
            free_models.append(model["id"])

    print("Found Free Models:")
    for m in free_models:
        print(f" - {m}")
except Exception as e:
    print("Failed:", e)
