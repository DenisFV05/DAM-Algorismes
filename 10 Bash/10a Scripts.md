# Bash

Un **Bash Script** és un fitxer de text que conté una sèrie d'instruccions que el sistema operatiu executa seqüencialment mitjançant el terminal. Es fa servir molt per automatitzar tasques en sistemes UNIX (Linux i macOS).

Les utilitats dels scripts *Bash* són:

- Automatitzar tasques repetitives (crear còpies de seguretat, processar fitxers).
- Escriure programes senzills que interactuen amb el sistema.
- Combinar comandes del terminal per simplificar tasques repetitives.

### Estructura

- **Shebang**: Sempre comença amb la línia *#!/bin/bash*, que diu quin programa ha d'executar el codi.
- **Instruccions**: Les comandes o el codi que executarem.

```bash
#!/bin/bash
echo "Hola, món!"
```

### Executar scripts 'bash'

Els scripts han de tenir permissos d'execució:

```bash
chmod +x nomScript.sh
```

S'executen com qualsevol altre arxiu executable, amb **./**:

```bash
./nomScript.sh
```

## Programació Bash

Com qualsevol altre llenguatge d'scripting, té elements de programació essencials:

### Variables

Per emmagatzemar informació:

```bash
#!/bin/bash
nom="Raquel"
echo "Hola, $nom!"
```

**Nota**: Fixeu-vos que no hi han espais al votant de *=*, al declarar la variable:

```bash
#!/bin/bash
nom = "Raquel"  # Incorrecte
```

### Condicionals

Per prendre decisions:

```bash
#!/bin/bash
if [ $1 -gt 10 ]; then
    echo "El número és més gran que 10."
else
    echo "El número és 10 o més petit."
fi
```

Les condicions s'escriuen entre claudàtors [ ] o dobles claudàtors [[ ]]

Comparacions habituals:

- **Números**: -eq, -ne, -gt, -lt, -ge, -le.
- **Cadenes**: = (iguals), != (diferents), -z (buit), -n (no buit).
- **Fitxers**: -e (existeix), -d (és directori), -f (és fitxer).

Exemple:

```bash
if [[ -z $1 ]]; then
    echo "No has passat cap argument."
elif [[ $1 -gt 10 ]]; then
    echo "El número és més gran que 10."
else
    echo "El número és 10 o més petit."
fi
```

### Bucles

Per repetir accions:

Bucle **for**:

```bash
for i in {1..5}; do
    echo "Número: $i"
done
```

Bucle **while**:

```bash
i=1
while [ $i -le 5 ]; do
    echo "Número: $i"
    i=$((i + 1))
done
```

### Funcions

Per dividir el codi en blocs

**Important**: les funcions només poden retornar **enters entre 0 i 255**:

```bash
comprova_numero() {
    if [[ $1 -gt 10 ]]; then
        return 1
    else
        return 0
    fi
}
comprova_numero 12
echo $? # Sortida: 1 (el número és més gran de 10)
```

Si es vol retornar un altre tipus de valor, s'ha de fer per cadena de text a través de la mateixa linia de comandes *(echo)*

```bash
saluda() {
    echo "Hola, $1!"
}

missatge=$(saluda "Raquel")
echo "$missatge"  # Sortida: Hola, Raquel!
```

### Paràmetres

Els paràmetres permeten passar informació a un script Bash des de la línia de comandes. 

Aquesta informació es pot utilitzar dins de l'script per personalitzar el seu comportament.

El **pas de paràmetres** es fa al cridar l'script per la línia de comandes:

```bash
./script.sh param1 param2 param3
```

Els paràmetres es *"reben"* com a variables anomenades *$1, $2, ..., $n*

```bash
#!/bin/bash
echo "Primer paràmetre: $1"
echo "Segon paràmetre: $2"
```

Al executar l'script anterior:

```bash
./script.sh hola món
# Sortida:
# Primer paràmetre: hola
# Segon paràmetre: món
```

Valors importants:

- **\$0** indica el nom de l'script
- **\$#** retorna el nombre total de paràmetres
- **\$@** retorna tots els paràmetres com una llista separada per espais
- **\$*** similar a $@, però tracta tots els paràmetres com una sola cadena

```bash
#!/bin/bash

# Cada paràmetre es tracta per separat.
for param in "$@"; do
    echo "$param"
done

# Tot es tracta com un sol paràmetre.
for param in "$*"; do
    echo "$param"
done
```

Verificar si hi han paràmetres:
```bash
#!/bin/bash
if [ $# -eq 0 ]; then
    echo "No s'han proporcionat paràmetres."
    exit 1
fi
```

Si no es passa un paràmetre, es pot definir un valor per defecte:
```bash
#!/bin/bash
nom=${1:-"Usuari"}  # Si $1 no està definit, usa "Usuari"
echo "Hola, $nom!"
```

## Script de super usuari

Per exigir que un script s'executi amb permissos de super usuari *(root)*:

```bash
#!/bin/bash

# Comprovar si l'usuari és root
if [[ $EUID -ne 0 ]]; then
    echo "Aquest script s'ha d'executar com a superusuari (root)." >&2
    exit 1
fi

# Afegir aquí les accions que necessiten permisos d'administrador.

echo "Script executat amb privilegis de superusuari."
```

## Data i hora

Per obtenir la data i hora des de Bash, es fa servir la comanda date amb l'opció + i un format personalitzat:

```bash
#!/bin/bash

# Obtenir data i hora actual
data_hora=$(date +"%Y-%m-%d_%H-%M-%S")
echo "Data i hora actual: $data_hora"

# Crear una carpeta amb aquesta data
mkdir "backup_$data_hora"
echo "S'ha creat la carpeta: backup_$data_hora"
```

**Format**:

- **%Y**: Any complet (ex. 2025)
- **%m**: Mes en format numèric (01-12)
- **%d**: Dia del mes (01-31)
- **%H**: Hora en format 24 hores (00-23)
- **%M**: Minuts (00-59)
- **%S**: Segons (00-59)

