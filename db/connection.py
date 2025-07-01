"""
Utilitaire de connexion à la base de données

Ce module contient la fonction `get_connection`, qui est responsable de l'établissement 
d'une connexion à une base de données PostgreSQL. Elle récupère les détails de connexion 
nécessaires (hôte, utilisateur, mot de passe, base de données, port) à partir des variables 
d'environnement en utilisant la bibliothèque `dotenv` pour les charger depuis un fichier `.env`.

La fonction utilise la bibliothèque `psycopg2` pour se connecter à la base de données 
PostgreSQL et retourne un objet de connexion qui peut être utilisé pour d'autres opérations 
sur la base de données.

Dépendances :
    - os
    - psycopg2
    - dotenv
"""

import os
import psycopg2                 # type:ignore
from dotenv import load_dotenv  # type:ignore


load_dotenv()

def get_connection():
    """
    Établit et retourne une connexion à la base de données PostgreSQL en utilisant 
    les identifiants stockés dans les variables d'environnement.
    
    Cette fonction charge les variables d'environnement depuis un fichier .env 
    et les utilise pour se connecter à la base de données PostgreSQL via psycopg2. 
    L'objet de connexion retourné peut être utilisé pour interagir avec la base de données.
    
    Retourne :
        psycopg2.extensions.connection : Un objet de connexion pour interagir 
        avec la base de données PostgreSQL.

    Lève :
        psycopg2.OperationalError : En cas de problème avec la connexion à la base de données 
        (par exemple, identifiants incorrects, hôte inaccessible, etc.).
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
        port=os.getenv("DB_PORT")
    )
