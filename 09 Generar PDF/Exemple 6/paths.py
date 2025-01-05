#!/usr/bin/env python3

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import math

filename = "paths.pdf"

c = canvas.Canvas(filename, pagesize=A4)
page_width, page_height = A4
margin = 50

# Dibuixar una estrella utilitzant paths
def draw_star(c, cx, cy, size, points=5, rotation=0):
    # Calcular els punts de l'estrella
    angle = (2 * math.pi) / points  # angle entre punts
    outer_points = []
    inner_points = []
    
    for i in range(points):
        # Punts exteriors
        x = cx + size * math.cos(i * angle - math.pi/2 + rotation)
        y = cy + size * math.sin(i * angle - math.pi/2 + rotation)
        outer_points.append((x, y))
        
        # Punts interiors (a meitat de distància)
        x = cx + (size/2) * math.cos((i + 0.5) * angle - math.pi/2 + rotation)
        y = cy + (size/2) * math.sin((i + 0.5) * angle - math.pi/2 + rotation)
        inner_points.append((x, y))
    
    # Crear el camí
    path = c.beginPath()
    path.moveTo(outer_points[0][0], outer_points[0][1])
    
    # Dibuixar l'estrella alternant punts exteriors i interiors
    for i in range(points):
        path.lineTo(inner_points[i][0], inner_points[i][1])
        path.lineTo(outer_points[(i+1)%points][0], outer_points[(i+1)%points][1])
    
    # Tancar i dibuixar el camí
    path.close()
    c.drawPath(path, stroke=1, fill=1)

# Dibuixar una forma ondulada amb curveTo
def draw_wave(c, x, y, width, height, waves=3):
    path = c.beginPath()
    path.moveTo(x, y)
    
    wave_width = width / waves
    for i in range(waves):
        # Punts de control per la corba
        x1 = x + (i * wave_width) + (wave_width * 0.25)
        y1 = y + height
        x2 = x + (i * wave_width) + (wave_width * 0.75)
        y2 = y + height
        x3 = x + (i + 1) * wave_width
        y3 = y
        
        path.curveTo(x1, y1, x2, y2, x3, y3)
    
    c.drawPath(path, stroke=1, fill=0)

def draw_pentagon(c, cx, cy, size, rotation=0):
    # Angles dels vèrtexs del pentàgon
    angle1 = math.radians(rotation)
    angle2 = angle1 + (2 * math.pi / 5)
    angle3 = angle2 + (2 * math.pi / 5)
    angle4 = angle3 + (2 * math.pi / 5)
    angle5 = angle4 + (2 * math.pi / 5)
    
    # Coordenades dels cinc vèrtexs
    x1, y1 = cx + size * math.cos(angle1), cy + size * math.sin(angle1)
    x2, y2 = cx + size * math.cos(angle2), cy + size * math.sin(angle2)
    x3, y3 = cx + size * math.cos(angle3), cy + size * math.sin(angle3)
    x4, y4 = cx + size * math.cos(angle4), cy + size * math.sin(angle4)
    x5, y5 = cx + size * math.cos(angle5), cy + size * math.sin(angle5)
    
    # Crear el camí
    path = c.beginPath()
    path.moveTo(x1, y1)
    path.lineTo(x2, y2)
    path.lineTo(x3, y3)
    path.lineTo(x4, y4)
    path.lineTo(x5, y5)
    path.close()
    
    # Dibuixar el pentàgon
    c.drawPath(path, stroke=1, fill=1)

# Dibuixar dues estrelles
c.setLineWidth(2)
c.setStrokeColor(HexColor("#FF5555"))
c.setFillColorRGB(0.9, 0.6, 0.1)
draw_star(c, page_width/2, page_height-200, 100, points=5, rotation=0)
c.setFillColorRGB(1.0, 1.0, 0.2, 0.5) # Semi transparent: alpha=0.5
draw_star(c, page_width/2 + 55, page_height-200, 75, points=5, rotation=75)


# Dibuixar ones
c.setLineWidth(3)
c.setStrokeColor(HexColor("#5555FF"))
draw_wave(c, margin, page_height/2, page_width-2*margin, 50, waves=4)

# Dibuixar un pentàgon al centre de la pàgina
c.setStrokeColorRGB(0, 0, 0) 
c.setFillColorRGB(0.6, 0.8, 0.2)
page_width, page_height = A4
draw_pentagon(c, 400, 150, 50, rotation=0)

# Dibuixar una forma oberta
c.setStrokeColorRGB(0, 0, 0) 
path = c.beginPath()
path.moveTo(100, 100) 
path.lineTo(200, 200) 
path.lineTo(250, 175)
path.lineTo(200, 125)
c.drawPath(path, stroke=1, fill=0)

# Guardar el PDF
c.save()
