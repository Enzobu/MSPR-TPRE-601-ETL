"""
Ce module permet de gérer les relations entre les pays et leurs types de climat dans une base de données.
Il inclut des fonctions pour récupérer les pays et types de climat existants, insérer des relations pays-climat 
dans la table `country_climat_type`, et gérer les données nécessaires à partir d'un fichier JSON et de la base 
de données.
"""

import json
from psycopg2.extras import execute_batch   # type: ignore

from db.connection import get_connection
from db.truncate_table import truncate_table


PAYS_REGION_JSON = "./json/pays_region.json"

def get_existing_countries():
    """
    Récupère les pays existants dans la base de données avec leurs ID.

    Cette fonction interroge la table `country` pour obtenir les pays existants et leurs ID associés.
    Elle retourne un dictionnaire où la clé est le nom du pays en minuscule et la valeur est son ID.

    Returns:
        dict: Dictionnaire avec les noms des pays en minuscule comme clés et les ID comme valeurs.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_country, name FROM country;")
    countries = {name.lower(): id for id, name in cursor.fetchall()}
    cursor.close()
    conn.close()
    return countries

def get_existing_climat_types():
    """
    Récupère les types de climat existants dans la base de données avec leurs ID.

    Cette fonction interroge la table `climat_type` pour obtenir les types de climat existants et leurs ID 
    associés.
    Elle retourne un dictionnaire où la clé est le nom du climat en minuscule et la valeur est son ID.

    Returns:
        dict: Dictionnaire avec les noms des types de climat en minuscule comme clés et les ID comme valeurs.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_climat_type, name FROM climat_type;")
    climat_types = {name.lower(): id for id, name in cursor.fetchall()}
    cursor.close()
    conn.close()
    return climat_types

def set_country_climat_types():
    """
    Insère les relations pays-climat dans la table pivot `country_climat_type`.

    Cette fonction charge les données des pays et de leurs climats depuis un fichier JSON. Elle récupère les 
    ID des pays et des types de climat depuis la base de données et insère les relations pays-climat dans la 
    table `country_climat_type`. Si un climat ou un pays n'existe pas dans la base de données, la relation est 
    ignorée.
    
    Si des erreurs se produisent pendant l'insertion, la transaction est annulée.

    Returns:
        None
    """
    with open(PAYS_REGION_JSON, "r", encoding="utf-8") as file:
        pays_data = json.load(file)

    country_map = get_existing_countries()
    climat_map = get_existing_climat_types()

    conn = get_connection()
    cursor = conn.cursor()

    truncate_table("country_climat_type")

    values = []
    for country_name, data in pays_data.items():
        country_id = country_map.get(country_name.lower())

        if not country_id:
            continue

        for climat in data["climat"]:
            climat_id = climat_map.get(climat.lower())
            if not climat_id:
                print(f"[WARNING] Climat '{climat}' non trouvé en base, ignoré.")
                continue
            values.append((country_id, climat_id))
            print(f"[INFO] Préparation de la relation pays-climat : {country_name} - {climat}")

    if not values:
        print("[ERROR] Aucun pays-climat valide à insérer.")
        return

    sql = """
        INSERT INTO country_climat_type (id_country, id_climat_type)
        VALUES (%s, %s);
    """
    try:
        execute_batch(cursor, sql, values)
        conn.commit()
        print(f"[INFO] {len(values)} relations pays-climat insérées dans 'country_climat_type'.")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Problème lors de l'insertion des pays-climats : {e}")
    finally:
        cursor.close()
        conn.close()
