from fastapi import FastAPI
from app.api.chat import router as chat_router

app = FastAPI(title="Jammi E-commerce Assistant")

app.include_router(chat_router)
