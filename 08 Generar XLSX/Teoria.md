<div style="display: flex; width: 100%;">
    <div style="flex: 1; padding: 0px;">
        <p>© Albert Palacios Jiménez, 2024</p>
    </div>
    <div style="flex: 1; padding: 0px; text-align: right;">
        <img src="./assets/ieti.png" height="32" alt="Logo de IETI" style="max-height: 32px;">
    </div>
</div>
<br/>

# Generar XLSX

A l'empresa, és habitual que s'hagin de generar arxius **Excel .XLSX** a partir de dades de manera automàtica. 

Els llenguatges de programació solen tenir llibreries que ho fan possible. A Python hi ha *xlsxwriter*:

```bash
pip install XlsxWriter
```

O bé a macOS o Linux amb *brew*:
```bash
python3 -m pip install XlsxWriter --break-system-package
```

## Arxius i fulls

Aquests són els objectes més significatius de la llibreria:

- **workbook**, representa un arxiu *Excel*
- **worksheet**, representa un full de càlcul

Al full dins de l'arxiu se li defineix un nom, a l'exemple és 'Full 0':

**Exemple 0**

```python
#!/usr/bin/env python3
import xlsxwriter

filename = 'hello.xlsx'

workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet('Full 0')

worksheet.write('A1', 'Hello world')

workbook.close()

print(f"Genearated: '{filename}'")
```

## Dades

Les dades s'escriuen amb **"worksheet.write"**, hi ha diverses maneres de fer-ho:

- Definint la columna i la fila estil 'D3'
```text
worksheet.write("D3", "Hola")
```

- Definint la columna i la fila numèricament
```python
# igual que D3
fila = 3
columna = 4 
worksheet.write(fila, columna, "Hola")
```

**Exemple 1**

```python
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
```

## Estils

Es pot canviar l'estil dels textos amb un estil al fer **.write**:

```python
my_format = workbook.add_format({
    'font_name': 'Arial',     # per canviar la font
    'font_size': 12,          # mida de la lletra
    'font_color': 'red',      # 'blue', 'green', etc.
    'bold': True,             # True/False
    'italic': True,           # True/False
    'underline': 1,           # 1 = underline, 2 = doble
    'align': 'center',        # 'left', 'right', 'justify'
    'valign': 'vcenter',      # 'top', 'bottom'
    'text_wrap': True,        # True/False
})
worksheet.write('A1', 'Text formatat', my_format)
```

L'estil també es pot definir per *cel·la*, *fila* i *columna* segons aquesta prioritat, per:

- Cel·la
- Fila
- Columna

```python
# 'B:B' vol dir tota la columna 'B'
italic = workbook.add_format({'italic': True})
worksheet.set_column('B:B', None, italic)

# Definir l'estil de la fila 0
bold = workbook.add_format({'bold': True})
worksheet.set_row(0, None, bold);
```

**Exemple 2**

```python
#!/usr/bin/env python3
import xlsxwriter



workbook.close()
print(f"Genearated: '{filename}'")
```