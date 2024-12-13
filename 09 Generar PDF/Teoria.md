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
<center><img src="./assets/context01.jpg" style="max-height: 400px" alt="">
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
pos_y = height - margin_v
c.drawString(margin_h, pos_y, "Primera pàgina - Horitzontal A4")

# Rectangle línia per marcar marges
c.rect(margin_h, margin_v, width - 2 * margin_h, height - 2 * margin_v)

# Tancar la pàgina actual i començar-ne una de nova
c.showPage()

# Definir la mida i horientació
# de la segona pàgina: vertical A4
c.setPageSize(A4)
width, height = A4

# Text de la pàgina
pos_y = height - margin_v
c.drawString(margin_h, pos_y, "Segona pàgina - Vertical A4")

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

Els estils de text en *reportlab* es defineixen mitjançant objectes de tipus **ParagraphStyle**. Aquests estils permeten configurar atributs com:

- Font (`fontName`, `fontSize`, `leading`)
- Colors (`textColor`, `backColor`)
- Marges (`leftIndent`, `rightIndent`, `spaceBefore`, `spaceAfter`)
- Alineació (`alignment`, amb valors com `TA_LEFT`, `TA_CENTER`, etc.)

```python
estilTitol = ParagraphStyle(
    name="MainTitle",
    fontName="Helvetica-Bold",
    fontSize=24,
    leading=30,
    textColor=custom_colors['primary'],
    alignment=TA_CENTER,
    spaceAfter=20,
)
```

A més s'accepta un petit conjunt d'elements HTML:

```html
# Formats bàsics
<b> - negreta
<i> - cursiva
<u> - subratllat
<strike> - text tatxat
<sub> - subíndex
<br/> - salt de línia
```

### Exemple 3: Definir i aplicar estils de text

```python
#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

filename = "styles.pdf"

# Definir una paleta de colors personalitzada
custom_colors = {
    'primary': colors.HexColor('#1B4F72'),
    'secondary': colors.HexColor('#2E86C1'),
    'accent1': colors.HexColor('#E74C3C'),
    'accent2': colors.HexColor('#27AE60'),
    'neutral': colors.HexColor('#566573'),
}

# Definir estils personalitzats amb més varietat
styles = {
    "MainTitle": ParagraphStyle(
        name="MainTitle",
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        textColor=custom_colors['primary'],
        alignment=TA_CENTER,
        spaceAfter=20,
    ),
    "Subtitle": ParagraphStyle(
        name="Subtitle",
        fontName="Helvetica-Oblique",
        fontSize=18,
        leading=22,
        textColor=custom_colors['secondary'],
        alignment=TA_CENTER,
        spaceAfter=15,
    ),
    "HeadingLeft": ParagraphStyle(
        name="HeadingLeft",
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=custom_colors['accent1'],
        alignment=TA_LEFT,
        spaceBefore=10,
        spaceAfter=8,
    ),
    "HeadingRight": ParagraphStyle(
        name="HeadingRight",
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=custom_colors['accent2'],
        alignment=TA_RIGHT,
        spaceBefore=10,
        spaceAfter=8,
    ),
    "BodyJustified": ParagraphStyle(
        name="BodyJustified",
        fontName="Helvetica",
        fontSize=12,
        leading=15,
        textColor=custom_colors['neutral'],
        alignment=TA_JUSTIFY,
        spaceBefore=6,
        spaceAfter=6,
        firstLineIndent=20,
    ),
    "BodyCenter": ParagraphStyle(
        name="BodyCenter",
        fontName="Helvetica",
        fontSize=12,
        leading=15,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceBefore=6,
        spaceAfter=6,
    ),
    "BodyLeft": ParagraphStyle(
        name="BodyLeft",
        fontName="Helvetica",
        fontSize=12,
        leading=15,
        textColor=custom_colors['neutral'],
        alignment=TA_LEFT,
        spaceBefore=6,
        spaceAfter=6,
        firstLineIndent=0,
    ),
    "Quote": ParagraphStyle(
        name="Quote",
        fontName="Helvetica-Oblique",
        fontSize=14,
        leading=18,
        textColor=custom_colors['secondary'],
        alignment=TA_CENTER,
        leftIndent=50,
        rightIndent=50,
        spaceBefore=15,
        spaceAfter=15,
    ),
    "Highlight": ParagraphStyle(
        name="Highlight",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.white,
        alignment=TA_CENTER,
        backColor=custom_colors['accent1'],
        borderPadding=10,
        spaceBefore=10,
        spaceAfter=10,
    ),
    "Strikethrough": ParagraphStyle(
        name="Strikethrough",
        fontName="Helvetica",
        fontSize=14,
        leading=18,
        textColor=custom_colors['neutral'],
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=8,
    ),
    "ListStyle": ParagraphStyle(
        name="ListStyle",
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=custom_colors['neutral'],
        alignment=TA_LEFT,
        spaceBefore=6,
        spaceAfter=6,
        leftIndent=30,  # Espai per als bullets
        bulletIndent=15,  # Posició dels bullets
    )
}

def draw_paragraph(c, text, style, x, y, width):
    p = Paragraph(text, style)
    _, height = p.wrap(width, float('inf'))
    p.drawOn(c, x, y - height)
    return height

def draw_bullet_list(c, items, style, x, y, width):
    for item in items:
        bullet_text = f"• {item}"
        p = Paragraph(bullet_text, style)
        _, height = p.wrap(width, float('inf'))
        p.drawOn(c, x, y - height)
        y -= (height + style.spaceBefore + style.spaceAfter)
    return y

# Crear el canvas
c = canvas.Canvas(filename, pagesize=A4)
page_width, page_height = A4
current_y = page_height - 50
margin = 50
width = page_width - (2 * margin)

# Exemples de text amb diferents estils
texts = [
    ("Exemple d'Estils de Text", "MainTitle"),
    ("Demostració de diferents formats i colors", "Subtitle"),
    ("Títol Alineat a l'Esquerra", "HeadingLeft"),
    ("""Aquest és un exemple de text justificat amb sagnat a la primera línia. 
    El text està formatat per ocupar tot l'ample disponible i crear marges 
    uniformes tant a la dreta com a l'esquerra. És útil per a documents 
    formals i text llarg.""", "BodyJustified"),
    ("Títol Alineat a la Dreta", "HeadingRight"),
    ("""Text centrat que mostra com es pot alinear el contingut al centre 
    de la pàgina. Útil per a subtítols i text destacat.""", "BodyCenter"),
    ("""«Aquesta és una cita destacada que utilitza un estil diferent 
    per cridar l'atenció del lector.»""", "Quote"),
    ("Text Destacat amb Fons de Color", "Highlight"),
    ("<strike>Text tatxat</strike>", "Strikethrough"),
    ("Exemple de Llista", "HeadingLeft"),
]

# Dibuixar cada text i actualitzar la posició vertical
for text, style_name in texts:
    height = draw_paragraph(c, text, styles[style_name], margin, current_y, width)
    current_y -= (height + styles[style_name].spaceBefore + styles[style_name].spaceAfter)

# Exemple de llista d'elements
list_items = [
    "Primer element de la llista amb <b>text en negreta</b>",
    "Segon element amb <i>text en cursiva</i>",
    "Tercer element amb <strike>text tatxat</strike>",
    "Quart element amb <u>text subratllat</u>",
    "Cinquè element amb un <sub>subíndex</sub>"
]

# Dibuixar la llista
current_y = draw_bullet_list(c, list_items, styles["ListStyle"], margin, current_y, width)

texts = [
    ("Exemple de <br/> salt de línia", "BodyLeft")
]

# Dibuixar cada text i actualitzar la posició vertical
for text, style_name in texts:
    height = draw_paragraph(c, text, styles[style_name], margin, current_y, width)
    current_y -= (height + styles[style_name].spaceBefore + styles[style_name].spaceAfter)


# Tancar i guardar
c.save()
```

Així es pot modularitzar i reutilitzar els estils en tot el document.

## Imatges

## Dibuix de formes