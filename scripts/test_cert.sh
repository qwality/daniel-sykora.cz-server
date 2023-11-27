#!/bin/bash

# Nastavíme pracovní adresář na adresář, ve kterém je umístěn skript
cd "$(dirname "$0")"

# Změníme cestu na relativní, předpokládáme, že složka .well-known je ve složce /home/cv/static
echo "$1" > ../static/.well-known/acme-challenge/test-file.txt
curl http://www.qwality.fun/.well-known/acme-challenge/test-file.txt
