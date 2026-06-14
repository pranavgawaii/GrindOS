import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY", "")

response = requests.get("https://openrouter.ai/api/v1/models", headers={"Authorization": f"Bearer {api_key}"})
models = response.json().get("data", [])

vision_models = []
for model in models:
    pricing = model.get("pricing", {})
    is_free = "free" in model["id"].lower() or (pricing.get("prompt", "-1") == "0" and pricing.get("completion", "-1") == "0")
    if is_free:
        # Check if it supports vision
        architecture = model.get("architecture", {})
        if architecture.get("modality", "") == "text+image->text" or "vl" in model["id"].lower() or "vision" in model["id"].lower() or "llama-3.2" in model["id"].lower() or "pixtral" in model["id"].lower() or "llava" in model["id"].lower():
            vision_models.append(model["id"])

print("Found Free Vision Models:")
for m in vision_models:
    print(f" - {m}")
