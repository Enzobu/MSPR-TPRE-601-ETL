#!/bin/bash

if ! command -v pylint &> /dev/null; then
    echo "Pylint n'est pas installé. Veuillez l'installer avant d'exécuter ce script."
    exit 1
fi

SRC_DIR="./"

if [ ! -d "$SRC_DIR" ]; then
    echo "Le dossier $SRC_DIR n'existe pas."
    exit 1
fi

find "$SRC_DIR" -type f -name "*.py" ! -name "__init__.py" | while read -r file; do
    echo "Analyse de $file avec pylint..."
    pylint "$file"
done
