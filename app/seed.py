from app import db
from app.models import CuratedReflection


def seed_curated_reflections():
    if CuratedReflection.query.first():
        return
    items = [
        {
            "titulo": "Confianza en medio de la tormenta",
            "referencia": "Salmos 46:1-2",
            "cita": "Dios es nuestro amparo y fortaleza, nuestro pronto auxilio en las tribulaciones.",
            "reflexion": "La fe no elimina las dificultades, pero nos recuerda que no caminamos solos. "
            "Anclar el corazón en quien es refugio verdadero trae paz que sobrepasa el entendimiento.",
            "orden": 1,
        },
        {
            "titulo": "Amor que da forma al día",
            "referencia": "1 Corintios 16:14",
            "cita": "Todas vuestras cosas hacedlas con amor.",
            "reflexion": "Pequeños actos de bondad, dichos con sinceridad y hechos con humildad, "
            "son el reflejo del amor de Cristo en lo cotidiano.",
            "orden": 2,
        },
        {
            "titulo": "Renovar la mente",
            "referencia": "Romanos 12:2",
            "cita": "No os conforméis a este siglo, sino transformaos por medio de la renovación de vuestro entendimiento.",
            "reflexion": "La transformación interior comienza al alinear pensamientos y decisiones con la verdad de Dios, "
            "paso a paso, con paciencia y gracia.",
            "orden": 3,
        },
        {
            "titulo": "Luz para el camino",
            "referencia": "Salmo 119:105",
            "cita": "Lámpara es a mis pies tu palabra, y lumbrera a mi camino.",
            "reflexion": "Cuando la incertidumbre pesa, la Escritura ilumina el siguiente paso: no siempre todo el mapa, "
            "pero la dirección suficiente para seguir.",
            "orden": 4,
        },
    ]
    for row in items:
        db.session.add(CuratedReflection(**row))
    db.session.commit()
