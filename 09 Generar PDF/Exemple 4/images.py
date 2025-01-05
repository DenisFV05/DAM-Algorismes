#!/usr/bin/env python3

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase.pdfmetrics import stringWidth

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

text_height = draw_paragraph(c, text, style, x + width + 10, y + height, width)

link_style = ParagraphStyle(
    name="BodyLeft",
    fontName="Helvetica",
    fontSize=12,
    leading=15,
    textColor='#00BBFF',
    alignment=TA_LEFT,
    spaceBefore=6,
    spaceAfter=6,
    firstLineIndent=0,
)
link_txt = "Més informació a Wikipedia"
link_url = "https://ca.wikipedia.org/wiki/Teckel"
link_x = x + width + 10
link_y = y + height - text_height - 10

# Dibuixar el text de l'enllaç i obtenir l'altura
link_height = draw_paragraph(c, "<u>" + link_txt + "</u>", link_style, link_x, link_y, width)

# Calcular les coordenades del rectangle de l'enllaç
# Les coordenades són (x1, y1, x2, y2) on:
# x1, y1 són la cantonada inferior esquerra
# x2, y2 són la cantonada superior dreta
link_width = stringWidth(link_txt, link_style.fontName, link_style.fontSize)
link_rect = (
    link_x,                    # x1
    link_y - link_height,      # y1
    link_x + link_width,       # x2
    link_y                     # y2
)

# Crear l'enllaç
c.linkURL(link_url, link_rect, relative=0)

# Guardar el PDF
c.save()