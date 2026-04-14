import json
import re

import google.generativeai as genai
from flask import current_app


def _configure():
    key = current_app.config.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "Falta GEMINI_API_KEY en la configuración. Añádela en el archivo .env para usar la generación con IA."
        )
    genai.configure(api_key=key)


def _humanize_gemini_error(error: Exception) -> str:
    text = str(error)
    upper = text.upper()
    if "API_KEY_INVALID" in upper or "API KEY NOT VALID" in upper:
        return (
            "La clave de Gemini no es válida. Corrige la variable `GEMINI_API_KEY` "
            "en Railway con una API key real de Google AI Studio."
        )
    if "PERMISSION_DENIED" in upper:
        return "Gemini rechazó la solicitud por permisos insuficientes. Revisa la API key configurada."
    if "QUOTA" in upper or "RATE LIMIT" in upper or "RESOURCE_EXHAUSTED" in upper:
        return "Gemini no pudo responder por límite de uso o cuota. Intenta de nuevo más tarde."
    return text


def is_quota_error(error: Exception) -> bool:
    upper = str(error).upper()
    return "QUOTA" in upper or "RATE LIMIT" in upper or "RESOURCE_EXHAUSTED" in upper


def generar_reflexion_biblica(tema_usuario: str | None, used_references: list[str] = None) -> dict:
    """
    Devuelve un dict con: cita_corta, referencia, reflexion (párrafo breve), tono, libro.
    """
    _configure()
    # Priorizamos 1.5-flash que suele tener cuotas más estables en el tier gratuito
    model_names = ("gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-2.0-flash")
    
    # Contexto de pasajes usados
    history_context = ""
    if used_references:
        history_context = f"\nPasajes ya usados (EVITA ESTOS): {', '.join(used_references[-15:])}"

    instruccion = f"""Eres un asistente cristiano respetuoso. Tu objetivo es generar una reflexión bíblica única.
{history_context}

Responde SOLO con un JSON válido, sin markdown:
"cita_corta": el versículo real,
"referencia": libro y pasaje (ej. "Salmos 23:1"),
"libro": nombre del libro (ej. "Salmos"),
"reflexion": 3-4 oraciones de aplicación pastoral,
"tono": una palabra (ej. esperanza).

Si el usuario pide un tema o libro, úsalo obligatoriamente. No repitas pasajes obvios."""

    if tema_usuario and tema_usuario.strip():
        user_part = f'Petición del usuario: "{tema_usuario.strip()}"'
    else:
        user_part = "Genera una reflexión libre y edificante."

    errores = []
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            resp = model.generate_content([instruccion, user_part])
            text = (getattr(resp, "text", None) or "").strip()
            
            # Limpieza y parseo
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text)
            data = json.loads(text)
            
            # Validación mínima
            for k in ("cita_corta", "referencia", "reflexion", "libro"):
                if k not in data or not str(data[k]).strip():
                    raise ValueError(f"Campo '{k}' faltante.")
            return data
        except Exception as e:
            if is_quota_error(e):
                errores.append("Gemini ha alcanzado su límite de uso gratuito por este minuto. Espera 60 segundos por favor.")
            else:
                errores.append(f"{name}: {str(e)}")
            continue
    
    if errores:
        # Mostramos un error limpio si es de cuota
        if "límite" in errores[0]:
            raise RuntimeError(errores[0])
        raise RuntimeError(f"Error en Gemini: {errores[0]}")
    raise RuntimeError("No se pudo obtener una reflexión en este momento.")
