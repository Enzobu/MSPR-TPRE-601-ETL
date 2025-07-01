"""
Ce module permet de gérer les maladies dans la base de données, y compris l'insertion des données dans la 
table `disease`. Il inclut une fonction pour insérer les informations des maladies à partir d'un 
dictionnaire dans la base de données après avoir vidé la table.
"""

import json
from psycopg2.extras import execute_batch   # type: ignore

from db.connection import get_connection
from db.truncate_table import truncate_table


DISEASE_JSON_FILE_PATH = 'json/disease.json'

def get_disease():
    """
    Charge un fichier JSON et le convertit en dictionnaire.

    Args:
        file_path (str): Le chemin du fichier JSON à charger.

    Returns:
        dict: Le contenu du fichier JSON sous forme de dictionnaire.
    """
    try:
        with open(DISEASE_JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"[ERROR] Le fichier '{DISEASE_JSON_FILE_PATH}' n'a pas été trouvé.")
    except json.JSONDecodeError:
        print("[ERROR] Erreur lors du décodage du fichier JSON.")
    except Exception as e:
        print(f"[ERROR] Une erreur est survenue : {e}")

def set_disease():
    """
    Insère les données des maladies dans la table `disease`.

    Cette fonction prend un dictionnaire de maladies, où chaque clé est le nom de la maladie et chaque 
    valeur est un dictionnaire contenant l'ID de la maladie et un indicateur si la maladie est pandémique. 
    Elle vide d'abord la table `disease` avec la fonction `truncate_table`, puis insère les données dans 
    la base de données via une requête SQL préparée.
    
    La fonction utilise `execute_batch` pour insérer les données en lot, ce qui améliore les performances 
    d'insertion pour un grand nombre de données.

    Args:
        disease (dict): Dictionnaire des maladies, où la clé est le nom de la maladie et la valeur est un 
        dictionnaire avec `id` et `isPandemic`.

    Returns:
        None
    """
    conn = get_connection()
    cursor = conn.cursor()

    truncate_table("disease")

    disease = get_disease()

    sql = "INSERT INTO disease (id_disease, name, is_pandemic) VALUES (%s, %s, %s)"

    values = [
        (data["id"], name.lower(), data["isPandemic"])
        for name, data in disease.items()
    ]

    execute_batch(cursor, sql, values)
    conn.commit()

    print("[INFO] Données insérées dans la table disease.")

    cursor.close()
    conn.close()
