from fastapi import APIRouter
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.ollama_service import generate_response
from app.services.conversation_service import get_conversation, add_message

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    session_id = request.session_id

    # Obtener historial
    history = get_conversation(session_id)

    # Agregar mensaje usuario
    add_message(session_id, "user", request.message)

    # Obtener historial actualizado
    updated_history = get_conversation(session_id)

    # Generar respuesta
    response = generate_response(updated_history)

    # Guardar respuesta del asistente
    add_message(session_id, "assistant", response)

    return ChatResponse(response=response)
