"""
Module pour l'insertion des types de climat dans la base de données.

Ce module charge les types de climat depuis un fichier JSON, nettoie la table 
'climat_type' dans la base de données, puis insère les données dans cette table.
Il utilise des requêtes SQL préparées et l'exécution par lots pour insérer les
données de manière efficace. Le fichier JSON à utiliser est défini dans la variable
CLIMAT_TYPE_JSON.

Fonctions principales :
- set_climat_type() : Charge les types de climat depuis le fichier JSON et les insère
  dans la base de données.
"""

import json
from psycopg2.extras import execute_batch   # type: ignore

from db.connection import get_connection
from db.truncate_table import truncate_table


CLIMAT_TYPE_JSON = "./json/climat_type.json"

def set_climat_type():
    """
    Insère les types de climat dans la base de données.
    
    Cette fonction charge les types de climat depuis un fichier JSON (CLIMAT_TYPE_JSON),
    nettoie la table 'climat_type' dans la base de données, puis insère les données de climat 
    dans la table en utilisant des requêtes SQL préparées pour une insertion par lot.

    Les étapes sont les suivantes :
    1. Chargement des données depuis le fichier JSON.
    2. Nettoyage de la table 'climat_type' pour éviter les doublons.
    3. Insertion des types de climat dans la base de données.
    
    Si une erreur survient à n'importe quelle étape, un message d'erreur est affiché
    et la transaction est annulée.

    Exceptions possibles :
    - Problèmes lors de l'ouverture du fichier JSON.
    - Erreurs lors de l'insertion dans la base de données ou de la connexion.
    """
    try:
        with open(CLIMAT_TYPE_JSON, "r", encoding="utf-8") as file:
            climat_types = json.load(file)
        print(f"[INFO] Chargement de {len(climat_types)} types depuis {CLIMAT_TYPE_JSON}.")
    except Exception as e:
        print(f"[ERROR] Impossible de charger {CLIMAT_TYPE_JSON}: {e}")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        truncate_table("climat_type")  # Nettoie la table avant insertion

        sql = """
            INSERT INTO climat_type (id_climat_type, name, description)
            VALUES (%s, %s, %s);
        """

        values = [(i + 1, climat["name"], climat["description"]) for i, climat in enumerate(climat_types)]

        execute_batch(cursor, sql, values)
        conn.commit()
        print(f"[INFO] {len(values)} types de climat insérés dans la table 'climat_type'.")

    except Exception as e:
        print(f"[ERROR] Problème lors de l'insertion des types de climat en base : {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
