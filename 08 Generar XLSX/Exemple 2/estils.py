#!/usr/bin/env python3
import xlsxwriter

filename = 'estils.xlsx'

workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet('Full 0')

# Definir l'estil de la fila 0
bold = workbook.add_format({'bold': True})
worksheet.set_row(0, None, bold);

# 'B:B' vol dir tota la columna 'B'
italic = workbook.add_format({'italic': True})
worksheet.set_column('B:B', None, italic)

# Combinar estils
bold_italic = workbook.add_format({'bold': True, 'italic': True})
worksheet.set_column('C:C', None, italic)

# Posar-hi dades
worksheet.write('A1', 'Nom')
worksheet.write('B1', 'Edat')
worksheet.write('C1', 'Població')

worksheet.write('A2', 'Miquel')
worksheet.write('B2', '24')
worksheet.write('C2', 'Cornellà')

worksheet.write('A3', 'Olga')
worksheet.write('B3', '22')
worksheet.write('C3', 'Hospitalet')

workbook.close()

print(f"Genearated: '{filename}'")

