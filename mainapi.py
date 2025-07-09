from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class TranslateRequest(BaseModel):
    text: str

@app.post("/translate")
def translate_text(data: TranslateRequest):
    response = requests.post(
        "https://api-inference.huggingface.co/models/t5-small",
        headers={},  # No token
        json={"inputs": f"translate Hindi to English: {data.text}"}
    )

    try:
        result = response.json()
    except Exception:
        return {
            "error": "Failed to decode Hugging Face response",
            "raw": response.text
        }

    if isinstance(result, list) and "translation_text" in result[0]:
        return {"translated": result[0]["translation_text"]}
    else:
        return {"error": result}
