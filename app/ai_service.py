import json
import re
from flask import current_app
from groq import Groq


def _get_client():
    key = current_app.config.get("GROQ_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "Falta GROQ_API_KEY en la configuración. Añádela en el archivo .env o en las variables de Railway para generar reflexiones."
        )
    return Groq(api_key=key)


def generar_reflexion_biblica(tema_usuario: str | None, used_references: list[str] = None) -> dict:
    """
    Devuelve un dict con: cita_corta, referencia, reflexion (párrafo breve), tono, libro.
    """
    client = _get_client()
    model_name = "llama-3.3-70b-versatile"
    
    history_context = ""
    if used_references:
        history_context = f"\nPasajes ya usados recientemente por el usuario (EVITA REPETIR ESTOS SI ES POSIBLE): {', '.join(used_references[-15:])}"

    instruccion = f"""Eres un asistente pastoral cristiano altamente capacitado. Tu objetivo es proporcionar una reflexión bíblica inspiradora.
{history_context}

Debes responder ÚNICA Y EXCLUSIVAMENTE con un objeto JSON válido (sin formato Markdown, sin texto extra), que contenga estas 5 claves:
"cita_corta": el versículo o segmento bíblico (fiel a las escrituras en español),
"referencia": libro y pasaje (ej. "Salmos 23:1"),
"libro": nombre formal del libro bíblico (ej. "Salmos", "1 Corintios"),
"reflexion": 3-4 oraciones de aplicación espiritual o pastoral profunda,
"tono": una sola palabra describiendo la emoción principal (ej. "esperanza", "fortaleza").

Si el usuario pide un tema o libro, úsalo obligatoriamente. Usa variedad en la Biblia."""

    if tema_usuario and tema_usuario.strip():
        user_part = f'Petición del usuario: "{tema_usuario.strip()}"'
    else:
        user_part = "Genera una reflexión libre y edificante sobre un pasaje hermoso."

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": instruccion},
                {"role": "user", "content": user_part}
            ],
            model=model_name,
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=600,
        )
        
        text = response.choices[0].message.content.strip()
        data = json.loads(text)
        
        # Validación mínima
        for k in ("cita_corta", "referencia", "reflexion", "libro", "tono"):
            if k not in data or not str(data.get(k, "")).strip():
                raise ValueError(f"Campo '{k}' faltante en la respuesta del AI.")
        return data
        
    except Exception as e:
        error_msg = str(e).lower()
        if "rate_limit" in error_msg or "rate limit" in error_msg:
            raise RuntimeError("Has alcanzado el límite de uso gratuito por este minuto. Espera un momento y vuelve a intentarlo.")
        elif "authentication_error" in error_msg or "invalid api key" in error_msg:
             raise RuntimeError("La API Key de Groq es inválida o no está configurada correctamente.")
        else:
             raise RuntimeError(f"Error de conexión con IA: {str(e)}")
