import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

def load_clients(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_pdf(client, output_path):
    """Genera un PDF personalizado basado en los datos del cliente."""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Nombre de la compañía en grande y azul
    c.setFont("Helvetica-Bold", 40)
    c.setFillColor(HexColor("#00008B"))
    c.drawString(50, height - 50, client['companyia'])

    # Texto principal
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor("#000000"))
    serveis_addicionals = ', '.join(f"{s['nom']} ({s['preu']} €)" for s in client['detall_cobraments']['serveis_addicionals'])
    text = (
        f"Estimad@ {client['nom']} {client['cognom']},\n\n"
        f"Ens dirigim a vostè per presentar-li el detall de la seva factura corresponent al mes de {client['mes_factura']}:\n\n"
    )
    text_x = 50
    text_y = height - 120
    for line in text.split("\n"):
        c.drawString(text_x, text_y, line)
        text_y -= 15

    # Detall dels Cobraments
    c.setFont("Helvetica-Bold", 14)
    c.drawString(text_x, text_y, "Detall dels Cobraments:")
    text_y -= 20

    c.setFont("Helvetica", 12)
    c.drawString(text_x, text_y, f"- Quota bàsica mensual: {client['detall_cobraments']['quota_basica']} €")
    text_y -= 15
    c.drawString(text_x, text_y, f"- Serveis addicionals: {serveis_addicionals}")
    text_y -= 15
    c.drawString(text_x, text_y, f"- Impostos aplicats (IVA): {client['detall_cobraments']['impostos']} €")
    text_y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(text_x, text_y, f"Total a pagar: {client['detall_cobraments']['total']} €")
    text_y -= 30

    # Mensaje adicional
    c.setFont("Helvetica", 12)
    additional_text = (
        "Recordi que pot consultar els detalls de les seves factures i gestionar els seus pagaments\n"
        "a través de l'àrea de clients al nostre lloc web o contactar amb el nostre servei\n"
        "d'atenció al client.\n\n"
        "Gràcies per confiar en nosaltres."
    )
    for line in additional_text.split("\n"):
        c.drawString(text_x, text_y, line)
        text_y -= 15

    # Firma ficticia
    text_y -= 20
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(text_x, text_y, "[Firma de la Companyia]")
    text_y -= 15
    c.drawString(text_x, text_y, "Atentament, Departament d'Atenció al Client")

    # Calendario
    text_y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(text_x, text_y, "Calendari de pagaments anual:")
    text_y -= 20

    c.setFont("Helvetica", 10)
    for mes, status in client['calendari_pagaments'].items():
        c.drawString(text_x, text_y, f"{mes}: {status}")
        text_y -= 12

    c.save()

# Cargar datos desde el archivo clients.json
data = load_clients('clients.json')

# Generar PDFs para todos los clientes
for i, client in enumerate(data['clients']):
    output_file = f"client_{i + 1}.pdf"
    generate_pdf(client, output_file)
    print(f"PDF generado: {output_file}")
