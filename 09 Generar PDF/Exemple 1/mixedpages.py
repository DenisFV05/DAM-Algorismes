#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

filename = 'mixedpages.pdf'

def cm_to_points(cm):
    return cm * 28.35

# Crear el canvas
c = canvas.Canvas(filename)

# Dimensions dels marges (passar cm a points)
margin_h = cm_to_points(1)  # 1 cm
margin_v = cm_to_points(2)  # 2 cm

# Definir la mida i horientació
# de la primera pàgina: horitzontal/landscape A4
c.setPageSize(landscape(A4))
width, height = landscape(A4)

# Text de la pàgina
pos_y = height - margin_v
c.drawString(margin_h, pos_y, "Primera pàgina - Horitzontal A4")

# Rectangle línia per marcar marges
c.rect(margin_h, margin_v, width - 2 * margin_h, height - 2 * margin_v)

# Tancar la pàgina actual i començar-ne una de nova
c.showPage()

# Definir la mida i horientació
# de la segona pàgina: vertical A4
c.setPageSize(A4)
width, height = A4

# Text de la pàgina
pos_y = height - margin_v
c.drawString(margin_h, pos_y, "Segona pàgina - Vertical A4")

# Rectangle per marcar marges
c.rect(margin_h, margin_v, width - 2 * margin_h, height - 2 * margin_v)

# Tancar i guardar
c.save()