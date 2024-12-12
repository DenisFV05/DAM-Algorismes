#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Path
from reportlab.graphics import renderPDF
import numpy as np
import bezier
import math

def get_path_points(start, end, control1, control2, num_points=100):
    """Calcula els punts al llarg d'una corba de Bézier."""
    nodes = np.asfortranarray([
        [start[0], control1[0], control2[0], end[0]],
        [start[1], control1[1], control2[1], end[1]]
    ])
    curve = bezier.Curve(nodes, degree=3)
    points = [curve.evaluate(t) for t in np.linspace(0, 1, num_points)]
    return points

def calculate_angle(p1, p2):
    """Calcula l'angle entre dos punts."""
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def draw_text_along_path(canvas, text, points, spacing_factor=1.0):
    """Dibuixa text seguint una sèrie de punts."""
    canvas.saveState()
    
    # Calculem l'espai necessari per cada caràcter
    total_length = sum(math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
                      for p1, p2 in zip(points[:-1], points[1:]))
    spacing = (total_length / len(text)) * spacing_factor
    
    current_distance = 0
    current_point_index = 0
    
    for char in text:
        # Trobem el punt actual
        while current_point_index < len(points) - 1:
            p1 = points[current_point_index]
            p2 = points[current_point_index + 1]
            segment_length = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            
            if current_distance + segment_length >= spacing:
                # Interpolem per trobar la posició exacta
                t = (spacing - current_distance) / segment_length
                x = p1[0] + t * (p2[0] - p1[0])
                y = p1[1] + t * (p2[1] - p1[1])
                angle = calculate_angle(p1, p2)
                
                # Dibuixem el caràcter rotat
                canvas.saveState()
                canvas.translate(x, y)
                canvas.rotate(math.degrees(angle))
                canvas.drawString(0, 0, char)
                canvas.restoreState()
                
                current_distance = 0
                break
            
            current_distance += segment_length
            current_point_index += 1
    
    canvas.restoreState()

def main():
    filename = "paths_example.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Crear el camí
    drawing = Drawing(width, height)
    path = Path()
    
    # Definim els punts de control
    start_point = (width/2 - 100, height/2)
    end_point = (width/2 + 100, height/2)
    control1 = (width/2 + 150, height/2 + 50)
    control2 = (width/2 - 150, height/2 + 50)
    
    path.moveTo(*start_point)
    path.lineTo(*end_point)
    path.curveTo(*control1, *control2, *start_point)
    drawing.add(path)
    
    # Dibuixem el camí
    renderPDF.draw(drawing, c, 0, 0)
    
    # Obtenim els punts del camí
    points1 = get_path_points(start_point, end_point,
                            (width/2, height/2), (width/2, height/2))
    points2 = get_path_points(end_point, start_point,
                            control1, control2)
    
    # Textos a afegir
    text1 = "Aquest és el primer text seguint un camí."
    text2 = "Aquest és el segon text seguint un camí diferent."
    
    # Dibuixem els textos seguint els camins
    draw_text_along_path(c, text1, points1, spacing_factor=1.2)
    draw_text_along_path(c, text2, points2, spacing_factor=1.2)
    
    c.save()

if __name__ == "__main__":
    main()