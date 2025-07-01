#!/bin/bash

# Affiche l'aide
function afficher_aide() {
  echo "Utilisation : $0 [NUMERO]"
  echo
  echo "Arguments :"
  echo "  NUMERO       Numéro du fichier à exécuter directement."
  echo "  -h           Affiche cette aide."
  echo
  echo "Si aucun argument n'est fourni, le script fonctionne en mode interactif."
  exit 0
}

if [ "$1" == "-h" ]; then
  afficher_aide
fi

options=($(find ./ -type f -name "*.py" | sort))

if [ ${#options[@]} -eq 0 ]; then
  echo "Aucun fichier .py trouvé dans le répertoire courant ou ses sous-dossiers."
  exit 1
fi

if [ -n "$1" ]; then
  if ! [[ "$1" =~ ^[0-9]+$ ]] || [ "$1" -lt 1 ] || [ "$1" -gt "${#options[@]}" ]; then
    echo "Choix invalide. Utilisez -h pour afficher l'aide."
    exit 1
  fi
  choix="$1"
else
  echo -e "\n\nVeuillez choisir un numéro dans la liste :"
  previous_dir=""
  for i in "${!options[@]}"; do
    current_dir=$(dirname "${options[i]}")
    if [ "$current_dir" != "$previous_dir" ]; then
      if [ "$i" -ne 0 ]; then
        echo ""
      fi
      previous_dir="$current_dir"
    fi
    echo "$((i + 1)). ${options[i]}"
  done

  echo -e "\n"
  read -p "Entrez le numéro correspondant à votre choix : " choix
  echo -e "\n"

  if ! [[ "$choix" =~ ^[0-9]+$ ]] || [ "$choix" -lt 1 ] || [ "$choix" -gt "${#options[@]}" ]; then
    echo "Choix invalide. Veuillez réessayer."
    exit 1
  fi
fi

fichier_a_executer="${options[$((choix - 1))]}"

echo -e "Exécution de : $fichier_a_executer\n"
# python3 "$fichier_a_executer"
# spark-submit "$fichier_a_executer"
spark-submit --jars /opt/spark/jars/postgresql-42.6.0.jar "$fichier_a_executer" > etl.log
