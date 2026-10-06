from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

app = FastAPI()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


@app.get("/")
def home():
    return {
        "message": "CounterWatch AI Engine is running!"
    }


@app.get("/test-gemini")
def test_gemini():
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="Reply with only: Gemini is working"
    )

    return {
        "result": response.text
    }


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):

    image_data = await file.read()

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[
            {
                "text": "Look at this image. Is there a person sitting on or occupying the chair/counter? Reply with ONLY one of these two results: PERSON_PRESENT or NO_PERSON."
            },
            {
                "inline_data": {
                    "mime_type": file.content_type,
                    "data": image_data
                }
            }
        ]
    )

    result = response.text.strip()

    return {
        "filename": file.filename,
        "result": result
    }