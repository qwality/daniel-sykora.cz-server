#!/bin/bash

# Nastavit absolutní cestu k složce skriptu
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Nastavit redeploy jako spustitelný
chmod +x "$SCRIPT_DIR/redeploy"

# Přidat cestu do proměnné PATH, pokud již není přidána
if ! grep -q "$SCRIPT_DIR/redeploy" ~/.bashrc; then
    echo 'export PATH="$PATH:'"$SCRIPT_DIR/redeploy"'"' >> ~/.bashrc
fi

# Aplikovat změny
source ~/.bashrc
