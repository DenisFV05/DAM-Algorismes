import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth

def load_clients(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_pdf(client, template_path, output_path):
    """Genera un PDF personalizado para un cliente."""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Título principal
    style_title = ParagraphStyle(
        name="Title",
        fontName="Helvetica-Bold",
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    title = f"FACTURA - {client['mes_factura']}"
    title_p = Paragraph(title, style_title)
    title_p.wrapOn(c, width - 100, height)
    title_p.drawOn(c, 50, height - 50)

    # Texto principal con márgenes
    text = f"""
    Estimad@ {client['nom']} {client['cognom']},

    Ens dirigim a vostè per presentar-li el detall de la seva factura corresponent al mes de {client['mes_factura']}:

    Detall dels Cobraments:
    - Quota bàsica mensual: {client['detall_cobraments']['quota_basica']} €
    - Serveis addicionals: {', '.join(f"{s['nom']} ({s['preu']} €)" for s in client['detall_cobraments']['serveis_addicionals'])}
    - Impostos aplicats (IVA): {client['detall_cobraments']['impostos']} €

    Total a pagar: {client['detall_cobraments']['total']} €

    Gràcies per confiar en nosaltres.
    """
    style_body = ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=12,
        leading=14,
        spaceBefore=10,
        spaceAfter=10
    )
    body_p = Paragraph(text, style_body)
    body_p.wrapOn(c, width - 100, height - 150)
    body_p.drawOn(c, 50, height - 200)

    # Firma ficticia
    c.drawString(50, 100, "[Firma de la companyia]")

    # Calendario como tabla
    calendar_data = [["Mes", "Estat del Pagament"]] + [[mes, status] for mes, status in client['calendari_pagaments'].items()]
    table = Table(calendar_data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table.wrapOn(c, width - 100, height - 400)
    table.drawOn(c, 50, 200)

    # Enlace al sitio
    website = "http://www.ieti.edu"
    link_text = "Departament d'Atenció al Client"
    link_width = stringWidth(link_text, "Helvetica", 12)
    c.drawString(50, 50, link_text)
    c.linkURL(website, (50, 45, 50 + link_width, 60), relative=0)

    c.save()

# Cargar datos desde el archivo clients.json
data = load_clients('clients.json')

# Generar PDFs para todos los clientes
for i, client in enumerate(data['clients']):
    output_file = f"client_{i + 1}.pdf"
    generate_pdf(client, "plantilla00.pdf", output_file)
    print(f"PDF generado: {output_file}")
