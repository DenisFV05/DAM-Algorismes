<div style="display: flex; width: 100%;">
    <div style="flex: 1; padding: 0px;">
        <p>© Albert Palacios Jiménez, 2024</p>
    </div>
    <div style="flex: 1; padding: 0px; text-align: right;">
        <img src="./assets/ieti.png" height="32" alt="Logo de IETI" style="max-height: 32px;">
    </div>
</div>
<br/>

# Generar PDF

A l'empresa, és habitual que s'hagin de generar arxius **Portable Document Format .pdf** a partir de dades de manera automàtica. 

Normalment són *cartes o documents* que s'envien a molts clients *amb dades personalitzades*, i es generen de manera automàtica.

Els llenguatges de programació solen tenir llibreries que ho fan possible. A Python hi ha *reportlab*:

```bash
pip install reportlab
```

O bé a macOS o Linux amb *brew*:
```bash
python3 -m pip install reportlab --break-system-package
```

## Arxius i canvas

Per crear un document *.pdf* amb *reportlab* només cal craer una superfície de dibuix **canvas** i escriure amb **drawString**.

Per definir la mida de la pàgina fem servir "A4" o la mida que ens calgui. Cada pàgina serà un *canvas* de dibuix*.

Al canvas si poden anar 'pintant' els objectes a sobre dels antics, així si volem netejar-lo i començar de nou:

<br/>
<center><img src="./assets/context00.png" style="max-height: 400px" alt="">
<br/></center>
<br/>
<br/>

Les coordenades del canvas de *reportlab* són **"Bottom-Left"** això vol dir que la posició (0,0) està a baix a l'esquerra.

<br/>
<center><img src="./assets/context01.png" style="max-height: 400px" alt="">
<br/></center>
<br/>
<br/>

**Exemple 0**

```python
#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

filename = 'hello.pdf'

# Crear el canvas
c = canvas.Canvas(filename, pagesize=A4)

# Afegir text a la pàgina
c.drawString(100, 750, "Hello World")

# Tancar i guardar el fitxer
c.save()
```

## Pàgines

Per definir la configuració de la pàgina, un cop creat el canvas, es fa:

```python
# Pàgina: horitzontal/landscape A4
c.setPageSize(landscape(A4))
width, height = landscape(A4)

# Pàgina: vertical A4
c.setPageSize(A4)
width, height = A4
```

Cal tenir en compte que es pot dibuixar a qualsevol part de la pàgina, així **si no es vol dibuixar fora dels 'marges' és el programador qui ha de vigilar** de no fer-ho

**Exemple 1**

```python
#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

filename = 'mixedpages.pdf'

def cm_to_points(cm):
    return cm * 28.35

# Crear el canvas
c = canvas.Canvas(filename)

# Dimensions dels marges (passar cm a points)
margin_h = cm_to_points(1)  # 1 cm
margin_v = cm_to_points(2)  # 2 cm

# Definir la mida i horientació
# de la primera pàgina: horitzontal/landscape A4
c.setPageSize(landscape(A4))
width, height = landscape(A4)

# Text de la pàgina
c.drawString(margin_h, height - margin_v, "Primera pàgina - Horitzontal A4")

# Rectangle línia per marcar marges
c.rect(margin_h, margin_v, width - 2 * margin_h, height - 2 * margin_v)

# Tancar la pàgina actual i començar-ne una de nova
c.showPage()

# Definir la mida i horientació
# de la segona pàgina: vertical A4
c.setPageSize(A4)
width, height = A4

# Text de la pàgina
c.drawString(margin_h, height - margin_v, "Segona pàgina - Vertical A4")

# Rectangle per marcar marges
c.rect(margin_h, margin_v, width - 2 * margin_h, height - 2 * margin_v)

# Tancar i guardar
c.save()
```

## Alineació de texts

Per fer textos alineats cal crear un **Pharagraph** amb un estil de text. A aquest objecte *pharagraph* cal definir-li la caixa que encapsula el text amb:

```python
# En aquest cas no es defineix cap limit d'altura
# fent servir "inf"
p.wrap(box["width"], float('inf')) 
```

Els tipus d'alineació són:

- **TA_LEFT**: Esquerra 
- **TA_CENTER**: Centrat 
- **TA_RIGHT**: Dreta 
- **TA_JUSTIFY**: Justificat 

**Exemple 2**

```python
#!/usr/bin/env python3

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

filename = "align.pdf"

def draw_text(c, box, text, alignment):
    # Configura l'estil del text
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.alignment = alignment

    # Crea el paràgraf i comprova si el text encaixa
    # Ajusta el text a l'ample i retorna l'espai necessari
    p = Paragraph(text, style)
    max_width, max_height = p.wrap(box["width"], float('inf'))  

    # Dibuixar el text ajustant l'origen a la part superior
    p.drawOn(c, box["x"], box["y"] - max_height)  

# Crear el canvas
c = canvas.Canvas(filename, pagesize=A4)

# Mides de la pàgina
page_width, page_height = A4

# Text Lorem Ipsum
lorem_text = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
)

# Configuració de marges i dimensions dels rectangles
rect_width = page_width / 2 - 50
rect_height = 100
margin_x = 50
margin_y = 50

# Definició dels rectangles com a diccionaris
rects = [
    {"x": margin_x, 
     "y": page_height - margin_y, 
     "width": rect_width - 10, 
     "height": rect_height, 
     "alignment": TA_LEFT, 
     "title": "Align left"},
    {"x": page_width - margin_x - rect_width, 
     "y": page_height - margin_y, 
     "width": rect_width - 10, 
     "height": rect_height, 
     "alignment": TA_CENTER, 
     "title": "Align center"},
    {"x": margin_x, 
     "y": page_height - 2 * (margin_y + rect_height), 
     "width": rect_width - 10, 
     "height": rect_height, 
     "alignment": TA_RIGHT, 
     "title": "Align right"},
    {"x": page_width - margin_x - rect_width, 
     "y": page_height - 2 * (margin_y + rect_height), 
     "width": rect_width - 10, 
     "height": rect_height, 
     "alignment": TA_JUSTIFY, 
     "title": "Align justify"},
]

# Dibuixar rectangles i textos
for rect in rects:
    # Dibuixa el rectangle
    c.rect(rect["x"], rect["y"] - rect["height"], rect["width"], rect["height"])
    # Escriu el títol
    draw_text(c, rect, rect["title"], TA_LEFT)
    # Escriu el text amb l'alineació especificada
    draw_text(c, {**rect, "y": rect["y"] - 20}, lorem_text, rect["alignment"])

# Tancar i guardar el PDF
c.save()
```

## Estils de texts


## Textos sobre camins (paths)

## Imatges

## Dibuix de formes