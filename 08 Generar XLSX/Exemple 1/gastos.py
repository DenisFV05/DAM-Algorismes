#!/usr/bin/env python3
import xlsxwriter

gastos = (
    ['Compra',   65],
    ['Barber',   15],
    ['Gasolina', 100],
    ['Gym',      70],
)

filename = 'gastos.xlsx'
workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet('Full 0')

# Fila de titol
worksheet.write(0, 0, 'Concepte')
worksheet.write(0, 1, 'Preu')

# Posar les dades
row = 2
for fila in gastos:
    worksheet.write(row, 0, fila[0])
    worksheet.write(row, 1, fila[1])
    row += 1

sumRow = len(gastos) + 4
worksheet.write(sumRow, 0, 'Total')
worksheet.write(sumRow, 1, f"=SUM(B1:B{len(gastos)})")

workbook.close()
print(f"Genearated: '{filename}'")
