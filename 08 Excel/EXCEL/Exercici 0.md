<div style="display: flex; width: 100%;">
    <div style="flex: 1; padding: 0px;">
        <p>© Albert Palacios Jiménez, 2024</p>
    </div>
    <div style="flex: 1; padding: 0px; text-align: right;">
        <img src="./assets/ieti.png" height="32" alt="Logo de IETI" style="max-height: 32px;">
    </div>
</div>
<br/>

# Exercici 0

Fes un script **python** que generi un arxiu *.xlsx* a partir de l'arxiu *notes.json* amb dades de notes.

El document ha de:

- Tenir dues pàgines, una amb les notes normals, la segona amb el codi d'alumne anònim.
- A la primera pàgina, la primera columna té el nom de l'alumne
- A la segona pàgina, la primera columna té els 4 números centrals de l'id
- A totes dues pàgines, la primera fila té els noms de l'activitat (PR01, EX01, ...)
- A totes dues pàgines, la segona fila té el valor de cada activitat en % 
- A totes dues pàgines, a partir de la segona columna i tercera fila ja hi ha les notes
- A totes dues pàgines, hi ha d'haver una columna "Vàlid" que diu si es pot fer mitjana o no es pot fer mitjana (no tenir més d'un 20% de faltes, i tenir més o igual a 4 de l'exàmen)
- A totes dues pàgines, hi ha d'haver una columna final amb el càlcul automàtic de la nota de l'alumne segons els % de la segona fila. Si no es compleixen les condicions per fer mitjana, la nota final serà un 1.
- A les columnes d'activitats (PR01, ... EX01) el color del text ha de ser vermell si es té menys d'un 5
- A la columna de notes finals, el fons ha de ser vermell si es té menys d'un 5 i verd si es té més o igual a 7

Els valors de les activitats són:

- PR01 10%
- PR02 10%
- PR03 10%
- PR04 20%
- EX01 50%

**Important**: Els càlculs dels valors i estils s'han de fer automàticament a l'excel, NO al codi pyhton.