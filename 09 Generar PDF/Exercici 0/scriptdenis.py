from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import json


def load_clients(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_pdf(client, output_path):
    """Genera un PDF personalizado basado en los datos del cliente."""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Línea verde en la parte superior y más gruesa
    c.setStrokeColor(HexColor("#40E0D0"))  # Establece el color turquesa claro
    c.setLineWidth(6)  # Aumenta el grosor de la línea (6 puntos)
    c.line(50, height - 20, width - 50, height - 20)  # Dibuja la línea en la parte superior de la página

    # Nombre de la compañía en grande y azul (moviéndolo un poquito más abajo)
    c.setFont("Helvetica-Bold", 40)
    c.setFillColor(HexColor("#00008B"))
    c.drawString(50, height - 60, client['companyia'])

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

    # **Segunda página para el calendario**
    c.showPage()  # Cambia a la segunda página

    # Título de la sección del calendario
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(HexColor("#00008B"))
    c.drawString(50, height - 50, "Calendari de Pagaments Anual:")

    # Leyenda del calendario
    c.setFont("Helvetica", 12)
    text_y = height - 80  # Comienza debajo del título

    # Leyenda: Definimos lo que significa cada color
    c.setFillColor(HexColor("#000000"))
    c.drawString(50, text_y, "Llegenda del Calendari:")
    text_y -= 20

    # Explicamos el significado de cada color
    c.setFillColor(HexColor("#000000"))  # Negro para el texto
    c.drawString(50, text_y, "Pagament regular:       ")
    c.setFillColor(HexColor("#00008B"))  # Azul
    c.drawString(250, text_y, "Bonificació del X%:     ")
    c.setFillColor(HexColor("#40E0D0"))  # Verde (turquesa claro)
    c.drawString(450, text_y, "Exempt de pagament:     ")
    text_y -= 20

    # Dibujamos un cuadro de color para que sea más claro
    c.setFillColor(HexColor("#000000"))  # Negro
    c.rect(150, text_y, 10, 10, fill=1)  # Rectángulo negro
    c.setFillColor(HexColor("#00008B"))  # Azul
    c.rect(350, text_y, 10, 10, fill=1)  # Rectángulo azul
    c.setFillColor(HexColor("#40E0D0"))  # Verde
    c.rect(550, text_y, 10, 10, fill=1)  # Rectángulo verde
    text_y -= 30

    # Establecer colores para los meses
    colores_mes = {
        "Pagament regular": "#000000",  # Negro
        "Bonificació del X%": "#00008B",  # Azul
        "Exempt de pagament": "#40E0D0",  # Verde
    }

    c.setFont("Helvetica", 12)
    # Dibujar los meses con su tipo de pago y color
    for i, (mes, status) in enumerate(client['calendari_pagaments'].items()):
        # Determinamos el color según el tipo de pago
        if "regular" in status.lower():
            color = "#000000"  # Negro
        elif "bonificació" in status.lower():
            color = "#00008B"  # Azul
        else:
            color = "#40E0D0"  # Verde

        c.setFillColor(HexColor(color))  # Establecemos el color correspondiente
        c.drawString(50, text_y, f"{mes}: {status}")
        text_y -= 20  # Espacio entre cada mes

    # Guardar el PDF
    c.save()



# Cargar datos desde el archivo clients.json
data = load_clients('09 Generar PDF/Exercici 0/clients.json')

# Generar PDFs para todos los clientes
for i, client in enumerate(data['clients']):
    output_file = f"client_{i + 1}.pdf"
    generate_pdf(client, output_file)
    print(f"PDF generado: {output_file}")
