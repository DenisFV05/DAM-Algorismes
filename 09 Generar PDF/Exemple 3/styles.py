#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

filename = "styles.pdf"

# Definir una paleta de colors personalitzada
custom_colors = {
    'primary': colors.HexColor('#1B4F72'),
    'secondary': colors.HexColor('#2E86C1'),
    'accent1': colors.HexColor('#E74C3C'),
    'accent2': colors.HexColor('#27AE60'),
    'neutral': colors.HexColor('#566573'),
}

# Definir estils personalitzats amb més varietat
styles = {
    "MainTitle": ParagraphStyle(
        name="MainTitle",
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        textColor=custom_colors['primary'],
        alignment=TA_CENTER,
        spaceAfter=20,
    ),
    "Subtitle": ParagraphStyle(
        name="Subtitle",
        fontName="Helvetica-Oblique",
        fontSize=18,
        leading=22,
        textColor=custom_colors['secondary'],
        alignment=TA_CENTER,
        spaceAfter=15,
    ),
    "HeadingLeft": ParagraphStyle(
        name="HeadingLeft",
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=custom_colors['accent1'],
        alignment=TA_LEFT,
        spaceBefore=10,
        spaceAfter=8,
    ),
    "HeadingRight": ParagraphStyle(
        name="HeadingRight",
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=custom_colors['accent2'],
        alignment=TA_RIGHT,
        spaceBefore=10,
        spaceAfter=8,
    ),
    "BodyJustified": ParagraphStyle(
        name="BodyJustified",
        fontName="Helvetica",
        fontSize=12,
        leading=15,
        textColor=custom_colors['neutral'],
        alignment=TA_JUSTIFY,
        spaceBefore=6,
        spaceAfter=6,
        firstLineIndent=20,
    ),
    "BodyCenter": ParagraphStyle(
        name="BodyCenter",
        fontName="Helvetica",
        fontSize=12,
        leading=15,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceBefore=6,
        spaceAfter=6,
    ),
    "BodyLeft": ParagraphStyle(
        name="BodyLeft",
        fontName="Helvetica",
        fontSize=12,
        leading=15,
        textColor=custom_colors['neutral'],
        alignment=TA_LEFT,
        spaceBefore=6,
        spaceAfter=6,
        firstLineIndent=0,
    ),
    "Quote": ParagraphStyle(
        name="Quote",
        fontName="Helvetica-Oblique",
        fontSize=14,
        leading=18,
        textColor=custom_colors['secondary'],
        alignment=TA_CENTER,
        leftIndent=50,
        rightIndent=50,
        spaceBefore=15,
        spaceAfter=15,
    ),
    "Highlight": ParagraphStyle(
        name="Highlight",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.white,
        alignment=TA_CENTER,
        backColor=custom_colors['accent1'],
        borderPadding=10,
        spaceBefore=10,
        spaceAfter=10,
    ),
    "Strikethrough": ParagraphStyle(
        name="Strikethrough",
        fontName="Helvetica",
        fontSize=14,
        leading=18,
        textColor=custom_colors['neutral'],
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=8,
    ),
    "ListStyle": ParagraphStyle(
        name="ListStyle",
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=custom_colors['neutral'],
        alignment=TA_LEFT,
        spaceBefore=6,
        spaceAfter=6,
        leftIndent=30,  # Espai per als bullets
        bulletIndent=15,  # Posició dels bullets
    )
}

def draw_paragraph(c, text, style, x, y, width):
    p = Paragraph(text, style)
    _, height = p.wrap(width, float('inf'))
    p.drawOn(c, x, y - height)
    return height

def draw_bullet_list(c, items, style, x, y, width):
    for item in items:
        bullet_text = f"• {item}"
        p = Paragraph(bullet_text, style)
        _, height = p.wrap(width, float('inf'))
        p.drawOn(c, x, y - height)
        y -= (height + style.spaceBefore + style.spaceAfter)
    return y

# Crear el canvas
c = canvas.Canvas(filename, pagesize=A4)
page_width, page_height = A4
current_y = page_height - 50
margin = 50
width = page_width - (2 * margin)

# Exemples de text amb diferents estils
texts = [
    ("Exemple d'Estils de Text", "MainTitle"),
    ("Demostració de diferents formats i colors", "Subtitle"),
    ("Títol Alineat a l'Esquerra", "HeadingLeft"),
    ("""Aquest és un exemple de text justificat amb sagnat a la primera línia. 
    El text està formatat per ocupar tot l'ample disponible i crear marges 
    uniformes tant a la dreta com a l'esquerra. És útil per a documents 
    formals i text llarg.""", "BodyJustified"),
    ("Títol Alineat a la Dreta", "HeadingRight"),
    ("""Text centrat que mostra com es pot alinear el contingut al centre 
    de la pàgina. Útil per a subtítols i text destacat.""", "BodyCenter"),
    ("""«Aquesta és una cita destacada que utilitza un estil diferent 
    per cridar l'atenció del lector.»""", "Quote"),
    ("Text Destacat amb Fons de Color", "Highlight"),
    ("<strike>Text tatxat</strike>", "Strikethrough"),
    ("Exemple de Llista", "HeadingLeft"),
]

# Dibuixar cada text i actualitzar la posició vertical
for text, style_name in texts:
    height = draw_paragraph(c, text, styles[style_name], margin, current_y, width)
    current_y -= (height + styles[style_name].spaceBefore + styles[style_name].spaceAfter)

# Exemple de llista d'elements
list_items = [
    "Primer element de la llista amb <b>text en negreta</b>",
    "Segon element amb <i>text en cursiva</i>",
    "Tercer element amb <strike>text tatxat</strike>",
    "Quart element amb <u>text subratllat</u>",
    "Cinquè element amb un <sub>subíndex</sub>"
]

# Dibuixar la llista
current_y = draw_bullet_list(c, list_items, styles["ListStyle"], margin, current_y, width)

texts = [
    ("Exemple de <br/> salt de línia", "BodyLeft")
]

# Dibuixar cada text i actualitzar la posició vertical
for text, style_name in texts:
    height = draw_paragraph(c, text, styles[style_name], margin, current_y, width)
    current_y -= (height + styles[style_name].spaceBefore + styles[style_name].spaceAfter)


# Tancar i guardar
c.save()

