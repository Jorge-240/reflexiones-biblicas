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


def generar_reflexion_biblica(tema_usuario: str | None) -> dict:
    """
    Devuelve un dict con: cita_corta, referencia, reflexion (párrafo breve), tono.
    """
    _configure()
    model_names = ("gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest")

    instruccion = """Eres un asistente cristiano respetuoso. Responde SOLO con un JSON válido, sin markdown, con estas claves exactas:
"cita_corta": una frase breve tomada o parafraseada fielmente de un pasaje bíblico reconocible (en español),
"referencia": referencia bíblica tipo "Juan 3:16" o "Salmos 23:1",
"reflexion":2 a 4 oraciones en español, tono cálido y pastoral, sin dogmatismo agresivo,
"tono": una sola palabra descriptiva del estado de ánimo (ej. esperanza, paz).

El contenido debe ser apropiado para toda la familia. No incluyas texto fuera del JSON."""
    if tema_usuario and tema_usuario.strip():
        user_part = f'Tema o contexto del usuario: "{tema_usuario.strip()}"'
    else:
        user_part = "Elige un tema general edificante (gratitud, confianza, servicio, perdón, etc.)."

    errores = []
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            resp = model.generate_content([instruccion, user_part])
            text = ""
            if resp.candidates:
                parts = []
                for c in resp.candidates:
                    if c.content and c.content.parts:
                        for p in c.content.parts:
                            if hasattr(p, "text") and p.text:
                                parts.append(p.text)
                text = "".join(parts).strip()
            if not text:
                text = (getattr(resp, "text", None) or "").strip()
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text)
            data = json.loads(text)
            for k in ("cita_corta", "referencia", "reflexion"):
                if k not in data or not str(data[k]).strip():
                    raise ValueError("Respuesta de IA incompleta.")
            return data
        except Exception as e:
            errores.append(f"{name}: {_humanize_gemini_error(e)}")
            continue
    if errores:
        first = errores[0].split(": ", 1)[1] if ": " in errores[0] else errores[0]
        raise RuntimeError(first)
    raise RuntimeError("No se pudo obtener una reflexión de Gemini en este momento.")
