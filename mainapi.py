from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Local2English API", description="Hindi to English Translator")

# Load translation pipeline without torch
translator = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-hi-en",
    device=-1  # force CPU usage, avoids torch dependency
)

class TranslateRequest(BaseModel):
    text: str

@app.post("/translate")
def translate_text(payload: TranslateRequest):
    result = translator(payload.text)
    return {"translated": result[0]["translation_text"]}
