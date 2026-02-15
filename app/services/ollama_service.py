import requests
from app.core.config import OLLAMA_URL, MODEL_NAME

def generate_response(messages: list) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "stream": False
        }
    )

    data = response.json()
    return data["message"]["content"]

