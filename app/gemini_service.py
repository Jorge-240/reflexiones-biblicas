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
    model_names = ("gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest")

    history_context = ""
    if used_references:
        # Solo enviamos las últimas 20 para no saturar el prompt pero dar variedad
        history_context = f"\nPasajes ya usados recientemente (EVITA ESTOS): {', '.join(used_references[-20:])}"

    instruccion = f"""Eres un asistente cristiano respetuoso y profundo. Tu objetivo es generar una reflexión bíblica única.
{history_context}

Responde SOLO con un JSON válido, sin markdown, con estas claves exactas:
"cita_corta": el versículo o frase bíblica real (fiel al texto original),
"referencia": libro, capítulo y versículo (ej. "Juan 3:16"),
"libro": solo el nombre del libro bíblico (ej. "Juan"),
"reflexion": un párrafo de 3 a 5 oraciones con una aplicación práctica y pastoral para el día a día,
"tono": una sola palabra (ej. esperanza, fortaleza, consuelo).

Condiciones:
1. Si el usuario pide un tema o libro, PRIORIZA ese contexto.
2. Si no pide nada, elige un pasaje poderoso y menos común para variar.
3. El contenido debe ser 100% bíblico y respetuoso.
4. No repitas pasajes obvios todo el tiempo."""

    if tema_usuario and tema_usuario.strip():
        user_part = f'Petición del usuario: "{tema_usuario.strip()}"'
    else:
        user_part = "Genera una reflexión libre y edificante."

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
            
            # Limpieza de JSON
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text)
            
            data = json.loads(text)
            for k in ("cita_corta", "referencia", "reflexion", "libro"):
                if k not in data or not str(data[k]).strip():
                    raise ValueError(f"Campo '{k}' faltante o vacío.")
            return data
        except Exception as e:
            errores.append(f"{name}: {str(e)}")
            continue
    
    if errores:
        raise RuntimeError(f"Error en Gemini: {errores[0]}")
    raise RuntimeError("No se pudo obtener una reflexión de Gemini.")
