from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI(title="Local2English API", description="Hindi to English Translator")

class TranslateRequest(BaseModel):
    text: str

@app.post("/translate")
def translate_text(payload: TranslateRequest):
    response = requests.post(
        "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-hi-en",
        headers={"Authorization": "Bearer hf_xxx"},  # optional, works without for small usage
        json={"inputs": payload.text}
    )
    result = response.json()
    if isinstance(result, list) and "translation_text" in result[0]:
        return {"translated": result[0]["translation_text"]}
    else:
        return {"error": result}
