from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/josevidelaolmos/Documents/local/clase-2")
OUT = ROOT / "infogramas"
OUT.mkdir(parents=True, exist_ok=True)

WIDTH = 1600
HEIGHT = 900

FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


TITLE = font(FONT_BLACK, 56)
SUBTITLE = font(FONT_REG, 28)
SECTION = font(FONT_BOLD, 34)
BODY = font(FONT_REG, 24)
BODY_BOLD = font(FONT_BOLD, 24)
SMALL = font(FONT_REG, 20)
SMALL_BOLD = font(FONT_BOLD, 20)


def rounded(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def shadow(draw: ImageDraw.ImageDraw, box, radius=28):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 10, y1 + 12, x2 + 10, y2 + 12), radius=radius, fill=(15, 23, 42, 28))


def bullet_list(draw, x, y, items, color, line_gap=18):
    for item in items:
        draw.ellipse((x, y + 9, x + 10, y + 19), fill=color)
        draw.text((x + 24, y), item, font=BODY, fill=color)
        y += 34 + line_gap
    return y


def wrapped_text(draw, text, xy, max_width, fill, font_obj, line_gap=10):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        probe = word if not current else f"{current} {word}"
        if draw.textlength(probe, font=font_obj) <= max_width:
            current = probe
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += font_obj.size + line_gap
    return y


def base_canvas(bg_top, bg_bottom):
    img = Image.new("RGBA", (WIDTH, HEIGHT), bg_bottom)
    px = img.load()
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = tuple(int(bg_top[i] * (1 - ratio) + bg_bottom[i] * ratio) for i in range(3)) + (255,)
        for x in range(WIDTH):
            px[x, y] = color
    return img


def card(draw, box, fill, outline):
    shadow(draw, box)
    rounded(draw, box, 28, fill, outline, 3)


def save(img, name):
    img.convert("RGB").save(OUT / name, quality=95)


def infographic_git():
    img = base_canvas((252, 243, 225), (255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    rounded(draw, (40, 40, 1560, 860), 34, (255, 252, 247), (226, 232, 240), 2)
    draw.text((90, 90), "Git y GitHub", font=TITLE, fill="#14213D")
    draw.text((90, 158), "Primero guardamos el trabajo. Después lo compartimos.", font=SUBTITLE, fill="#475569")

    card(draw, (90, 240, 740, 590), (255, 247, 237), "#F59E0B")
    draw.text((130, 285), "Git", font=SECTION, fill="#9A3412")
    wrapped_text(draw, "La herramienta que guarda el historial del proyecto en tu máquina.", (130, 345), 540, "#7C2D12", BODY)
    bullet_list(draw, 130, 405, [
        "registra cambios",
        "permite volver a versiones anteriores",
        "ordena el trabajo del proyecto",
    ], "#7C2D12", 10)

    card(draw, (860, 240, 1510, 590), (239, 246, 255), "#3B82F6")
    draw.text((900, 285), "GitHub", font=SECTION, fill="#1D4ED8")
    wrapped_text(draw, "La plataforma online donde publicamos repositorios y colaboramos.", (900, 345), 540, "#1E3A8A", BODY)
    bullet_list(draw, 900, 405, [
        "guarda el repo remoto",
        "permite compartir código",
        "conecta desarrollo con despliegue",
    ], "#1E3A8A", 10)

    draw.rounded_rectangle((140, 660, 1460, 810), radius=26, fill=(241, 245, 249), outline="#CBD5E1", width=2)
    draw.text((180, 695), "Escribir código", font=SMALL_BOLD, fill="#0F172A")
    draw.text((470, 695), "git add", font=SMALL_BOLD, fill="#0F172A")
    draw.text((710, 695), "git commit", font=SMALL_BOLD, fill="#0F172A")
    draw.text((1010, 695), "git push", font=SMALL_BOLD, fill="#0F172A")
    draw.text((1245, 695), "GitHub", font=SMALL_BOLD, fill="#1D4ED8")
    for x1, x2 in [(350, 450), (590, 690), (860, 960), (1120, 1220)]:
        draw.line((x1, 710, x2, 710), fill="#94A3B8", width=6)
        draw.polygon([(x2 - 18, 696), (x2 + 2, 710), (x2 - 18, 724)], fill="#94A3B8")

    save(img, "01-git-vs-github.png")


def infographic_app():
    img = base_canvas((236, 253, 245), (243, 244, 246))
    draw = ImageDraw.Draw(img, "RGBA")

    rounded(draw, (40, 40, 1560, 860), 34, (251, 255, 253), (209, 250, 229), 2)
    draw.text((90, 90), "¿Qué es una aplicación?", font=TITLE, fill="#16302B")
    draw.text((90, 158), "Levantar una app es poner un server a correr y responder pedidos.", font=SUBTITLE, fill="#4B5563")

    colors = [
        ((110, 250, 390, 510), (236, 253, 245), "#10B981", "Código", "La receta", "app.py"),
        ((430, 250, 710, 510), (239, 246, 255), "#3B82F6", "Runtime", "El cocinero", "Python"),
        ((750, 250, 1030, 510), (255, 247, 237), "#F59E0B", "Librerías", "Ingredientes listos", "Flask"),
        ((1070, 250, 1350, 510), (245, 243, 255), "#8B5CF6", "Terminal", "La orden para levantarla", "python app.py"),
    ]
    for box, fill, border, title, desc, example in colors:
        card(draw, box, fill, border)
        x1, y1, x2, y2 = box
        draw.text((x1 + 30, y1 + 34), title, font=SECTION, fill=border)
        draw.text((x1 + 30, y1 + 95), desc, font=BODY_BOLD, fill="#334155")
        draw.text((x1 + 30, y1 + 150), "Ejemplo", font=SMALL_BOLD, fill="#64748B")
        draw.text((x1 + 30, y1 + 185), example, font=BODY, fill="#0F172A")

    draw.line((300, 570, 800, 650), fill="#94A3B8", width=8)
    draw.line((570, 570, 800, 650), fill="#94A3B8", width=8)
    draw.line((890, 570, 800, 650), fill="#94A3B8", width=8)
    draw.line((1210, 570, 800, 650), fill="#94A3B8", width=8)
    draw.rounded_rectangle((450, 640, 1150, 805), radius=30, fill="#16302B")
    draw.text((620, 690), "Server web corriendo", font=SECTION, fill="#FFFFFF")
    draw.text((575, 735), "escucha pedidos del navegador", font=BODY, fill="#D1FAE5")
    draw.text((595, 770), "y devuelve una respuesta", font=BODY, fill="#D1FAE5")

    save(img, "02-que-es-una-app.png")


def infographic_local_cloud():
    img = base_canvas((248, 250, 252), (255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    rounded(draw, (40, 40, 1560, 860), 34, (255, 255, 255), (226, 232, 240), 2)
    draw.text((90, 90), "Local vs Cloud", font=TITLE, fill="#0F172A")
    draw.text((90, 158), "La misma app cambia según dónde corre y quién la administra.", font=SUBTITLE, fill="#475569")

    columns = [
        ((90, 240, 500, 720), (254, 242, 242), "#EF4444", "Local / On-Premise", "#7F1D1D", [
            "corre en tu notebook",
            "tú administras todo",
            "si apagas la máquina, se cae",
        ], "Ideal para aprender y hacer pruebas."),
        ((595, 240, 1005, 720), (255, 247, 237), "#F59E0B", "EC2 / IaaS", "#7C2D12", [
            "AWS te da una VM",
            "tú instalas SO, Python y app",
            "más control, más operación",
        ], "Se parece a alquilar un servidor en la nube."),
        ((1100, 240, 1510, 720), (239, 246, 255), "#2563EB", "Lambda / Serverless", "#1E3A8A", [
            "AWS opera infraestructura",
            "tú subes el código",
            "menos trabajo operativo",
        ], "Te enfocas más en la lógica que en el servidor."),
    ]
    for box, fill, border, title, text_color, bullets, closing in columns:
        card(draw, box, fill, border)
        x1, y1, x2, y2 = box
        draw.text((x1 + 32, y1 + 32), title, font=SECTION, fill=border)
        bullet_list(draw, x1 + 32, y1 + 120, bullets, text_color, 20)
        draw.text((x1 + 32, y2 - 125), "Idea clave", font=BODY_BOLD, fill=border)
        wrapped_text(draw, closing, (x1 + 32, y2 - 88), 320, text_color, BODY)

    draw.rounded_rectangle((140, 765, 1460, 820), radius=22, fill="#E2E8F0")
    draw.text((230, 780), "La pregunta central es: quién administra qué parte de la solución.", font=SMALL_BOLD, fill="#0F172A")

    save(img, "03-local-vs-cloud.png")


def infographic_models():
    img = base_canvas((239, 246, 255), (255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    rounded(draw, (40, 40, 1560, 860), 34, (255, 255, 255), (191, 219, 254), 2)
    draw.text((90, 90), "Modelos de despliegue", font=TITLE, fill="#111827")
    draw.text((90, 158), "No toda nube se consume igual. Depende de control, costo y operación.", font=SUBTITLE, fill="#4B5563")

    items = [
        ((90, 250, 500, 710), (238, 242, 255), "#6366F1", "Nube pública", "#312E81",
         "Infraestructura compartida del proveedor.", ["rápida de usar", "pagas por consumo", "ejemplos: AWS, Azure, GCP"]),
        ((595, 250, 1005, 710), (236, 253, 245), "#10B981", "Nube privada", "#065F46",
         "Infraestructura dedicada a una organización.", ["más control", "más responsabilidad", "ejemplo: datacenter propio"]),
        ((1100, 250, 1510, 710), (255, 247, 237), "#F59E0B", "Nube híbrida", "#92400E",
         "Combina entorno local con recursos cloud.", ["mezcla dos mundos", "útil por seguridad o costo", "ejemplo: datos locales + app en AWS"]),
    ]
    for box, fill, border, title, text_color, summary, bullets in items:
        card(draw, box, fill, border)
        x1, y1, x2, y2 = box
        draw.text((x1 + 32, y1 + 32), title, font=SECTION, fill=border)
        wrapped_text(draw, summary, (x1 + 32, y1 + 105), 330, text_color, BODY_BOLD)
        bullet_list(draw, x1 + 32, y1 + 220, bullets, text_color, 20)

    draw.rounded_rectangle((120, 760, 1480, 820), radius=20, fill="#111827")
    draw.text((250, 778), "No existe un único modelo correcto: depende del nivel de control y operación que necesitas.", font=SMALL_BOLD, fill="#F9FAFB")

    save(img, "04-modelos-de-despliegue.png")


if __name__ == "__main__":
    infographic_git()
    infographic_app()
    infographic_local_cloud()
    infographic_models()
