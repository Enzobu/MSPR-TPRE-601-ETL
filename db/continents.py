"""
Continent Data Insertion

Ce module contient la fonction `set_continents`, qui insère les noms des 
continents dans la table 'continent' de la base de données. La fonction commence 
par nettoyer la table (truncation) et insère ensuite les données des continents 
en évitant les doublons à l'aide de la clause SQL `ON CONFLICT (name) DO NOTHING`.

Dépendances :
    - psycopg2.extras (execute_batch)
    - db.connection (get_connection)
    - db.truncate_table (truncate_table)

Les continents insérés sont :
    - "Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", 
      "South America".
"""

from psycopg2.extras import execute_batch   # type: ignore

from db.connection import get_connection
from db.truncate_table import truncate_table


def set_continents():
    """
    Insère les noms des continents dans la table 'continent' de la base de données.

    Cette fonction commence par nettoyer la table 'continent' en utilisant la 
    fonction `truncate_table`. Ensuite, elle insère les noms des continents dans 
    la table 'continent'. Si un continent existe déjà dans la table, l'opération 
    d'insertion est ignorée grâce à la clause `ON CONFLICT (name) DO NOTHING`.

    Le processus inclut les continents suivants : "Africa", "Antarctica", "Asia", 
    "Europe", "North America", "Oceania", "South America".

    Les étapes suivantes sont exécutées dans cette fonction :
    1. Truncate la table 'continent'.
    2. Insertion des données.
    3. Commit des changements dans la base de données.

    Exceptions :
        - Si une erreur survient lors de l'insertion des données, un message d'erreur
          est affiché et les changements sont annulés (rollback).
    
    Returns:
        None
    """
    truncate_table("continent")

    continents = [
        "Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America"
    ]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = "INSERT INTO continent (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;"
        values = [(continent.lower(),) for continent in continents]

        execute_batch(cursor, sql, values)
        conn.commit()
        print(f"[INFO] {len(continents)} continents insérés dans la table 'continent'.")

    except Exception as e:
        print(f"[ERROR] Problème lors de l'insertion des continents : {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
