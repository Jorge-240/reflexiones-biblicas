import json
from flask import current_app
from google import genai
from google.genai import types

def _get_gemini_client():
    key = current_app.config.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "Falta GEMINI_API_KEY en la configuración. Añádela en el archivo .env o en las variables de Render para generar reflexiones."
        )
    return genai.Client(api_key=key)


def generar_reflexion_biblica(tema_usuario: str | None, used_references: list[str] = None) -> dict:
    """
    Devuelve un dict con: cita_corta, referencia, reflexion (párrafo breve), tono, libro.
    """
    client = _get_gemini_client()
    
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
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"{instruccion}\n\n{user_part}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.7,
                max_output_tokens=600,
            ),
        )
        
        text = response.text.strip()
        data = json.loads(text)
        
        # Validación mínima
        for k in ("cita_corta", "referencia", "reflexion", "libro", "tono"):
            if k not in data or not str(data.get(k, "")).strip():
                raise ValueError(f"Campo '{k}' faltante en la respuesta del AI.")
        return data
        
    except Exception as e:
        error_msg = str(e).lower()
        if "quota" in error_msg or "rate limit" in error_msg or "429" in error_msg:
            raise RuntimeError("Has alcanzado el límite de uso de la API de Gemini. Espera un momento y vuelve a intentarlo.")
        elif "api_key" in error_msg or "invalid" in error_msg or "400" in error_msg:
             raise RuntimeError("La API Key de Gemini es inválida o no está configurada correctamente.")
        else:
             raise RuntimeError(f"Error de conexión con IA: {str(e)}")
