# Backups

Els backups permeten guardar informació d'un disc **en moments determinats**.

Sistemes de còpies de seguretat com **[Time Machine](https://en.wikipedia.org/wiki/Time_Machine_%28macOS%29)** de *macOS*, creen una còpia incremental del contingut d'una carpeta. *[Vídeo](https://www.youtube.com/watch?v=KMUUQCPuRHg)*

Això vol dir que es guarden les modificacions en una linia de temps, per recuperar l'estat d'un disc **en un moment específic**.

Es fa amb enllaços [links](https://en.wikipedia.org/wiki/Symbolic_link) per evitar duplicar fitxers que no han canviat, estalviant espai i mantenint una estructura fàcil de navegar.

## Avantatges

- **Eficiència d'espai**: Només es copien fitxers nous o modificats.
- **Velocitat**: Els enllaços simbòlics es creen ràpidament.
- **Accés senzill**: Les còpies semblen completes i són fàcils de navegar.

## Funcionament

1 - Primera còpia completa:

- Es copia tot el contingut de l'origen a la destinació.


2 - Còpies incrementals:

- Es comparen els fitxers de l'origen amb l'última còpia.
- Si un fitxer no ha canviat, es crea un enllaç simbòlic al fitxer existent en comptes de copiar-lo.
- Si un fitxer ha canviat, es copia completament.

3- Enllaços simbòlics:

- Són referències a fitxers o carpetes existents.
- Es creen amb la comanda ln -s.
- Estalvien espai al disc perquè només ocupen bytes per a la referència, no el fitxer complet.


4- Estructura:

- Cada còpia es guarda en una carpeta amb una marca de temps (backup_YYYY-MM-DD_HH-MM-SS).
- Aquesta estructura permet accedir fàcilment a qualsevol punt de restauració.

**Implementació en Bash**

Els passos principals per implementar-ho en Bash:

- Comprovar l'existència de la carpeta d'origen i destí.
- Crear una carpeta nova per a la còpia, amb la data i hora actual.
- Comparar els fitxers de l'origen amb l'última còpia:

    * Si el fitxer ja existeix i no ha canviat → Crear un enllaç simbòlic.
    * Si el fitxer no existeix o ha canviat → Copiar-lo.

- Registrar els errors en un fitxer de registre.

