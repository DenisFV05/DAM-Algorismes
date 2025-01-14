#!/usr/bin/env python3
import xlsxwriter
import json

# Archivo de salida
filename = 'notes.xlsx'
workbook = xlsxwriter.Workbook(f"{filename}")

# Hojas
worksheet = workbook.add_worksheet('Full 0')
worksheet1 = workbook.add_worksheet('Full 1')

# Títulos y datos base
titols = ["Name", "PR01", "PR02", "PR03", "PR04", "EX01", "%Faltes", "Valid", "Nota Final"]
titols_pag_2 = ["ID", "PR01", "PR02", "PR03", "PR04", "EX01", "%Faltes", "Valid", "Nota Final"]
percentatges = [10, 10, 10, 20, 50]

# Estilos
bold = workbook.add_format({'bold': True, 'align': 'center'})
red_text = workbook.add_format({'font_color': 'red'})
green_background = workbook.add_format({'bg_color': '#00FF00', 'font_color': 'black'})
red_background = workbook.add_format({'bg_color': '#FF0000', 'font_color': 'black'})
percent_format = workbook.add_format({'num_format': '0%'})

# Función para aplicar estilos condicionales
def aplicar_estils_condicionals(full):
    full.conditional_format("B3:F1000", {  # Notas individuales en rojo si son < 5
        'type': 'cell',
        'criteria': '<',
        'value': 5,
        'format': red_text
    })
    full.conditional_format("I3:I1000", {  # Nota final: rojo < 5
        'type': 'cell',
        'criteria': '<',
        'value': 5,
        'format': red_background
    })
    full.conditional_format("I3:I1000", {  # Nota final: verde >= 7
        'type': 'cell',
        'criteria': '>=',
        'value': 7,
        'format': green_background
    })

# Leer datos del JSON
with open('08 Excel/EXCEL/notes.json') as f:
    data = json.load(f)

# Escribir encabezados y porcentajes en ambas hojas
for ws, titols in [(worksheet, titols), (worksheet1, titols_pag_2)]:
    ws.write_row(0, 0, titols, bold)
    ws.write_row(1, 1, [f"{p}%" for p in percentatges], percent_format)

# Escribir datos en Full 0
fila = 2
for element in data:
    worksheet.write(fila, 0, element["Name"])  # Nombre del alumno
    for col, key in enumerate(["PR01", "PR02", "PR03", "PR04", "EX01"], start=1):
        worksheet.write(fila, col, element[key])
    worksheet.write(fila, 6, element["%Faltes"])  # % Faltes

    # Fórmulas para "Valid" y "Nota Final"
    worksheet.write_formula(fila, 7, f'=IF(AND(F{fila + 1} >= 4, G{fila + 1} <= 20), "Valid", "No Valid")')
    weights = "+".join([f"B{fila + 1}*B2", f"C{fila + 1}*C2", f"D{fila + 1}*D2", f"E{fila + 1}*E2", f"F{fila + 1}*F2"])
    worksheet.write_formula(fila, 8, f'=IF(H{fila + 1}="Valid", {weights}, 1)')
    fila += 1

# Escribir datos en Full 1 (ID Anónimo)
fila = 2
for element in data:
    anon_id = element["id"][3:7]  # Extraer los 4 dígitos centrales del ID
    worksheet1.write(fila, 0, anon_id)
    for col, columna in enumerate(["B", "C", "D", "E", "F"], start=1):
        worksheet1.write_formula(fila, col, f"'Full 0'!{columna}{fila + 1}")  # Copiar valores de Full 0
    worksheet1.write_formula(fila, 6, f"'Full 0'!G{fila + 1}")  # % Faltes
    worksheet1.write_formula(fila, 7, f"'Full 0'!H{fila + 1}")  # Valid
    worksheet1.write_formula(fila, 8, f"'Full 0'!I{fila + 1}")  # Nota Final
    fila += 1

aplicar_estils_condicionals(worksheet)
aplicar_estils_condicionals(worksheet1)

# Guardar el archivo
workbook.close()
print(f"Generated: '{filename}'")
