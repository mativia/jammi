import os

# Permitir sobreescribir vía variables de entorno
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL_NAME = os.getenv("MODEL_NAME", "phi3:mini")