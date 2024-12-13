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

Fes un script **python** que generi 5 arxius *.pdf* a partir de l'arxiu *clients.json* amb cartes personalitzades per cada client.

Els documents han de:

- Crear un .pdf mida A4 per cada client amb les seves dades
- Fer servir la plantilla indicada per cada alumne
- El text "Departament ..." **ha d'enllaçar** cap a la web de l'institut
- Afegir una imatge la firma de la companyia (inventada)
- Mostrar el calendari segons les dades de cada client
- **Tots** els calendaris han de tenir forma de calendari i una llegenda (encara que no surti a la plantilla)

El text que s'ha de mostrar a la carta adaptat a cada client és el següent:
```text
Estimad@ [Nom del Client] [Cognom del Client],

Ens dirigim a vostè per presentar-li el detall de la seva factura corresponent al mes de [Mes de la Factura]:

Detall dels Cobraments

- Quota bàsica mensual: [Import de la Quota Bàsica]

- Serveis addicionals: [Llista de serveis amb preus]

- Impostos aplicats (IVA): [Import dels impostos]

Total a pagar: [Preu Final] €

Li recordem el calendari de pagaments anual segons el seu pla contractat:

[Calendari del tipus de pagament segons més]

Llegenda del calendari:

[Quadre blanc] - Pagament regular
[Quadre blau] - Bonificació del X%
[Quadre verd] - Exempt de pagament

Recordi que pot consultar els detalls de les seves factures i gestionar els seus pagaments a través de l'àrea de clients al nostre lloc web o contactar amb el nostre servei d'atenció al client al [Número de Telèfon].

Gràcies per confiar en nosaltres.

Atentament,

[Nom de la Companyia Telefònica]
Departament d'Atenció al Client
```

**Relació de plantilles i alumnes**

```text
plantilla00.pdf - Daniel Artiaga
plantilla01.pdf - Adrià Martínez
plantilla02.pdf - Mario Pes
plantilla03.pdf - Jonathan Rueda
plantilla04.pdf - Pablo Vicente
plantilla05.pdf - David Bargados
plantilla06.pdf - Daniel Hirch
plantilla07.pdf - Daniel Juarez
```
