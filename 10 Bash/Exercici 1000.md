# Exercici 1001

**Part A**: Saludar amb un paràmetre

Escriu un script **scr1000A_saluda.sh** que saludi l'usuari pel seu nom. Si no es passa cap nom com a paràmetre, utilitza "Usuari" com a valor per defecte.

La sortida ha de ser "Hola, ???"

Requisits:

- Fer servir variables i paràmetres.
- Verificar si s'ha passat un paràmetre.

**Part B**: Comprovar si un número és parell o senar

Escriu un script **scr1000B_parell.sh** que comprovi si el primer paràmetre és un número parell o senar.

Requisits:

- Ús de condicional amb comparacions.
- Validació de l'entrada. 

**Part C**: Llistar els fitxers més grans d'una carpeta

Escriu un script **scr1000C_fitxers.sh** que mostri els 5 fitxers més grans de la carpeta actual, ordenats per mida.

Requisits:

- Ús de comandes del sistema ([du](https://man7.org/linux/man-pages/man1/du.1.html), [sort](https://man7.org/linux/man-pages/man1/sort.1.html) i [head](https://man7.org/linux/man-pages/man1/head.1.html)).
- Fer servir [pipes |](https://en.wikipedia.org/wiki/Pipeline_(Unix)) per combinar comandes. 

**Part D**: Comptar el nombre d'arxius en subcarpetes

Escriu un script **scr1000D_comptador.sh** que recorri totes les subcarpetes a partir de la carpeta actual i mostri quants arxius conté cadascuna.

Requisits:

- Fer servir un bucle for per recórrer subcarpetes.
- Utilitzar comandes com find. 

**Part E**: Controlar l'execució com a superusuari

Escriu un script **scr1000E_sudo.sh** que només es pugui executar com a superusuari. Si l'usuari no és root, ha de mostrar un missatge d'error i sortir.

Requisits:

- Comprovar el valor de $EUID.
- Incloure un missatge d'error i una sortida controlada. 

