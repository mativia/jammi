import json
import logging
from typing import Any

import requests

from app.core.config import OLLAMA_URL, MODEL_NAME

logger = logging.getLogger(__name__)


def _extract_content(data: Any) -> str:
    if not isinstance(data, dict):
        return str(data)

    # common pattern: {"message": {"content": "..."}}
    msg = data.get("message")
    if isinstance(msg, dict):
        content = msg.get("content")
        if isinstance(content, str):
            return content

    # top-level fields
    for key in ("response", "content", "text"):
        if key in data and isinstance(data[key], str):
            return data[key]

    # choices / outputs arrays
    for arr_key in ("choices", "outputs", "output"):
        arr = data.get(arr_key)
        if isinstance(arr, list) and len(arr) > 0:
            first = arr[0]
            if isinstance(first, dict):
                # try nested message
                fm = first.get("message")
                if isinstance(fm, dict) and isinstance(fm.get("content"), str):
                    return fm.get("content")
                for k in ("content", "text"):
                    if k in first and isinstance(first[k], str):
                        return first[k]

    # fallback to JSON string
    try:
        return json.dumps(data)
    except Exception:
        return str(data)


def generate_response(messages: list) -> str:
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "messages": messages, "stream": False},
            timeout=30,
        )
    except Exception as e:
        logger.exception("Error conectando a Ollama: %s", e)
        return f"Error: no se pudo conectar al modelo ({e})"

    if resp.status_code != 200:
        logger.error("Ollama devolvió status %s: %s", resp.status_code, resp.text)
        return f"Error del modelo: status {resp.status_code} - {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        logger.error("Respuesta no JSON de Ollama: %s", resp.text)
        return f"Error: respuesta no JSON del modelo: {resp.text}"

    try:
        content = _extract_content(data)
    except Exception:
        logger.exception("Error extrayendo contenido de la respuesta: %s", data)
        content = str(data)

    return content

