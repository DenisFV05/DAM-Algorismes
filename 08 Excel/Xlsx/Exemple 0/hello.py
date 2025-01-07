#!/usr/bin/env python3
import xlsxwriter

filename = 'hello.xlsx'

workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet('Full 0')

worksheet.write('A1', 'Hello world')

workbook.close()

print(f"Genearated: '{filename}'")

