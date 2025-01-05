#!/usr/bin/env python3

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

filename = 'hello.pdf'

# Crear el canvas
c = canvas.Canvas(filename, pagesize=A4)

# Afegir text a la pàgina
c.drawString(100, 750, "Hello World")

# Tancar i guardar el fitxer
c.save()

