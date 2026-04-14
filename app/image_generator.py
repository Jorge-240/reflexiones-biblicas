import os
import textwrap
import uuid

from PIL import Image, ImageDraw, ImageFont


def _resolve_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\segoepr.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def crear_tarjeta_reflexion(
    *,
    cita: str,
    referencia: str,
    reflexion: str,
    output_dir: str,
    ancho: int = 1080,
    alto: int = 1350,
) -> str:
    """
    Crea una imagen tipo tarjeta y devuelve la ruta relativa desde static/ (ej. generated/uuid.png).
    """
    os.makedirs(output_dir, exist_ok=True)
    fname = f"{uuid.uuid4().hex}.png"
    abs_path = os.path.join(output_dir, fname)

    img = Image.new("RGB", (ancho, alto), (18, 24, 38))
    draw = ImageDraw.Draw(img)

    for y in range(alto):
        r = int(18 + (45 - 18) * (y / alto))
        g = int(24 + (58 - 24) * (y / alto))
        b = int(38 + (92 - 38) * (y / alto))
        draw.line([(0, y), (ancho, y)], fill=(r, g, b))

    margin = 72
    gold = (212, 175, 55)
    soft = (230, 232, 240)

    font_title = _resolve_font(42)
    font_ref = _resolve_font(32)
    font_body = _resolve_font(34)
    font_small = _resolve_font(26)

    y = margin + 40
    draw.text((margin, y), "Reflexión bíblica", font=font_title, fill=gold)
    y += 70

    cita_wrapped = textwrap.fill(cita.strip(), width=28)
    for line in cita_wrapped.split("\n"):
        draw.text((margin, y), line, font=font_body, fill=soft)
        y += int(getattr(font_body, "size", 28) * 1.35) + 4

    y += 20
    draw.text((margin, y), f"— {referencia}", font=font_ref, fill=gold)
    y += int(getattr(font_ref, "size", 24) * 1.6) + 30

    reflex_wrapped = textwrap.fill(reflexion.strip(), width=32)
    for line in reflex_wrapped.split("\n"):
        draw.text((margin, y), line, font=font_small, fill=(200, 204, 218))
        y += int(getattr(font_small, "size", 22) * 1.3) + 2

    draw.rectangle([margin - 8, margin - 8, ancho - margin + 8, alto - margin + 8], outline=gold, width=3)

    img.save(abs_path, "PNG", optimize=True)
    return f"generated/{fname}"
