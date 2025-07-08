from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Local2English API", description="Hindi to English Translator")

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-hi-en")

class TranslateRequest(BaseModel):
    text: str

@app.post("/translate")
def translate_text(payload: TranslateRequest):
    result = translator(payload.text)
    return {"translated": result[0]["translation_text"]}
