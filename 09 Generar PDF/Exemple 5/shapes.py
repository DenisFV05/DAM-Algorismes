#!/usr/bin/env python3

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

filename = "shapes.pdf"
c = canvas.Canvas(filename, pagesize=A4)

# Mides de la pàgina
page_width, page_height = A4

# Dibuixar una línia
c.setLineWidth(4)
c.setStrokeColor(HexColor("#55AAFF"))
c.setStrokeColorRGB(0, 0, 0)
c.line(100, 50, 300, 250)

# Dibuixar un rectangle
c.setStrokeColorRGB(0.2, 0.5, 0.8) 
c.setFillColorRGB(0.8, 0.2, 0.2)
c.setLineWidth(15)
c.rect(100, 600, 200, 100, stroke=1, fill=1)

# Dibuixar un cercle
c.setLineWidth(5)
c.setStrokeColor(HexColor("#FFAA55"))
c.setFillColorRGB(0.3, 0.6, 0.3)
c.circle(300, 500, 50, stroke=1, fill=1)

# Dibuixar una el·lipse
c.setFillColorRGB(0.4, 0.2, 0.6)
c.ellipse(100, 300, 250, 350, stroke=0, fill=1)

c.save()
