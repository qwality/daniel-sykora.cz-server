#!/bin/bash

# Získání ID procesu pomocí ps aux a grep
process_id=$(ps aux | grep "uvicorn" | grep -v "grep" | awk '{print $2}' | head -n 1)

# Kontrola, zda bylo získáno ID procesu
if [ -n "$process_id" ]; then
    # Vypsání ID procesu
    echo "Nalezený proces Uvicorn s ID: $process_id"

    # Ukončení procesu pomocí kill
    echo "Ukončování procesu..."
    kill "$process_id"
    echo "Proces byl ukončen."
else
    echo "Proces Uvicorn nebyl nalezen."
fi