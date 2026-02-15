from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "jammi-ecommerce",
            "prompt": request.message,
            "stream": False
        }
    )

    data = response.json()
    return {"response": data["response"]}
