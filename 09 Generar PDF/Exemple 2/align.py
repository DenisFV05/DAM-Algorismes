#!/usr/bin/env python3

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

filename = "align.pdf"

def draw_text(c, box, text, alignment):
    # Configura l'estil del text
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.alignment = alignment

    # Crea el paràgraf i comprova si el text encaixa
    # Ajusta el text a l'ample i retorna l'espai necessari
    p = Paragraph(text, style)
    max_width, max_height = p.wrap(box["width"], float('inf'))  

    # Dibuixar el text ajustant l'origen a la part superior
    p.drawOn(c, box["x"], box["y"] - max_height)  

# Crear el canvas
c = canvas.Canvas(filename, pagesize=A4)

# Mides de la pàgina
page_width, page_height = A4

# Text Lorem Ipsum
lorem_text = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
)

# Configuració de marges i dimensions dels rectangles
rect_width = page_width / 2 - 50
rect_height = 100
margin_x = 50
margin_y = 50

# Definició dels rectangles com a diccionaris
rects = [
    {"x": margin_x, 
     "y": page_height - margin_y, 
     "width": rect_width - 10, 
     "height": rect_height, 
     "alignment": TA_LEFT, 
     "title": "Align left"},
    {"x": page_width - margin_x - rect_width, 
     "y": page_height - margin_y, 
     "width": rect_width - 10, 
     "height": rect_height, 
     "alignment": TA_CENTER, 
     "title": "Align center"},
    {"x": margin_x, 
     "y": page_height - 2 * (margin_y + rect_height), 
     "width": rect_width - 10, 
     "height": rect_height, 
     "alignment": TA_RIGHT, 
     "title": "Align right"},
    {"x": page_width - margin_x - rect_width, 
     "y": page_height - 2 * (margin_y + rect_height), 
     "width": rect_width - 10, 
     "height": rect_height, 
     "alignment": TA_JUSTIFY, 
     "title": "Align justify"},
]

# Dibuixar rectangles i textos
for rect in rects:
    # Dibuixa el rectangle
    c.rect(rect["x"], rect["y"] - rect["height"], rect["width"], rect["height"])
    # Escriu el títol
    draw_text(c, rect, rect["title"], TA_LEFT)
    # Escriu el text amb l'alineació especificada
    draw_text(c, {**rect, "y": rect["y"] - 20}, lorem_text, rect["alignment"])

# Tancar i guardar el PDF
c.save()
