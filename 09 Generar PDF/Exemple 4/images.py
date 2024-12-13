#!/usr/bin/env python3

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

filename = "with_image.pdf"

def draw_paragraph(c, text, style, x, y, width):
    p = Paragraph(text, style)
    _, height = p.wrap(width, float('inf'))
    p.drawOn(c, x, y - height)
    return height

c = canvas.Canvas(filename, pagesize=A4)

# Afegir una imatge
image_path = "dachshund.png" 
x = 50 
y = 550 
width = 200 
height = 250  
c.drawImage(image_path, x, y, width, height, None, True)

# Afegir comentari
style = ParagraphStyle(
    name="BodyLeft",
    fontName="Helvetica",
    fontSize=12,
    leading=15,
    textColor='#566573',
    alignment=TA_LEFT,
    spaceBefore=6,
    spaceAfter=6,
    firstLineIndent=0,
)
text = """
El dachshund, també dit <b>teckel</b> o gos salsitxa, és una raça de gos. 
<br/><br/>Té tres varietats: de pèl curt, de pèl dur i de pèl llarg.
<br/><br/>Aquesta raça tenia com a funció atrapar rosegadors sota terra i dins dels caus, d'aquí la seva forma allargada i baixa, amb una cua llarga i dura que s'emprava en tant que tirador. 
"""

draw_paragraph(c, text, style, x + width + 10, y + height, width)

# Guardar el PDF
c.save()
