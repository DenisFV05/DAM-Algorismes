# Exercici 1000

Escriu un script **Bash** que faci còpies de seguretat d'una carpeta d'origen cap a una carpeta de destí, tal i com ho fa **[Time Machine](https://en.wikipedia.org/wiki/Time_Machine_%28macOS%29)** de *macOS*. Aprofitant la comanda [rsync](https://linux.die.net/man/1/rsync) de UNIX.

Amb *rsync* es pot evitar crear duplicats d'arxius que ja existeixen al *backup*, fent servir enllaços a través del paràmetre **--link-dest**.

Pots fer servir [aquest article](https://samuelhewitt.com/blog/2018-06-05-time-machine-style-backups-with-rsync) com a base, tot i que els requeriments de l'exercici són lleugerament diferents i ho hauràs d'adaptar. 

## Paràmetres d'entrada:

```bash
./backup.sh <carpeta_origen> <carpeta_desti>
```

L'script ha de rebre com a paràmetres:

- **carpeta_origen**, les dades que per les que s'ha de fer una còpia de seguretat en el moment actual

- **carpeta_desti**, la carpeta on s'han de guardar/afegir les dades/modificacions.

## Requisits:

- Si la carpeta d'origen no existeix, l'script ha de mostrar un missatge d'error i sortir.
- Si la carpeta destí no existeix, l'ha de crear
- Cada còpia s'ha de guardar en una subcarpeta dins de la carpeta de destí amb un nom basat en la data i hora (backup_YYYY-MM-DD_HH-MM-SS).
- Els fitxers que no han canviat entre còpies s'han de substituir per enllaços simbòlics.
- Els fitxers nous o modificats s'han de copiar completament.
- Registra un fitxer de registre amb errors, si n'hi ha (backup.log).

**Sortida esperada:** mostrar informació del procés de còpia de seguretat

- Carpeta creada per a la còpia.
- Nombre de fitxers copiats i enllaçats.
- Missatge d'error en cas de problemes amb permisos o carpetes.

Les còpies de seguretat hauràn de permetre accedir a l'estat de la carpeta en un moment del temps determinat.

Fes servir aquest article 