from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class TranslateRequest(BaseModel):
    text: str

@app.post("/translate")
def translate_text(data: TranslateRequest):
    response = requests.post(
        "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-hi-en",
        headers={},  # 🚫 Make sure this is an **empty dict**, no Authorization!
        json={"inputs": data.text}
    )

    try:
        result = response.json()
    except Exception:
        return {
            "error": "Failed to decode response from Hugging Face.",
            "text": response.text
        }

    if isinstance(result, list) and "translation_text" in result[0]:
        return {"translated": result[0]["translation_text"]}
    else:
        return {"error": result}
