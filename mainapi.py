from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="Local2English API", description="Hindi to English Translator")

# Load token from environment variable
HF_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

class TranslateRequest(BaseModel):
    text: str

@app.post("/translate")
def translate_text(payload: TranslateRequest):
    response = requests.post(
        "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-hi-en",
        headers=headers,
        json={"inputs": payload.text}
    )

    try:
        result = response.json()
    except Exception as e:
        return {
            "error": "Response was not valid JSON",
            "status_code": response.status_code,
            "text": response.text
        }

    # Successful case
    if isinstance(result, list) and "translation_text" in result[0]:
        return {"translated": result[0]["translation_text"]}

    # API returned error JSON
    return {"error": result}
