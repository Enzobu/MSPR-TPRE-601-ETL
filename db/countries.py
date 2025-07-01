"""
Ce module permet de récupérer des données sur les pays, leur climat et leur PIB, 
et de les insérer dans une base de données. 
Les données sont extraites via des API externes (comme Restcountries et API Ninjas) 
et des fichiers JSON locaux.
"""

import json
import time
import requests # type: ignore
from psycopg2.extras import execute_batch   # type: ignore

from db.connection import get_connection
from db.truncate_table import truncate_table
from db.pib import fetch_gdp_data
from db.country_climat_type import set_country_climat_types


API_KEY = "UKRG6rVwuY8wXXfyE1ZWhg==Pu6zZccZayVbGrZi"
GDP_API_URL = "https://api.api-ninjas.com/v1/gdp?year=2020"

PAYS_REGION_JSON = "./json/pays_region.json"

def get_countries_from_api() :
    """
    Récupère les données des pays depuis l'API Restcountries.

    Cette fonction envoie une requête GET à l'API Restcountries pour récupérer les informations sur tous les pays.
    Si la requête est réussie, elle retourne les données des pays sous forme de liste JSON.
    En cas d'erreur, elle affiche un message d'erreur et retourne None.

    Returns:
        list or None: Liste des pays si la requête réussit, sinon None.
    """
    try:
        code = 500
        while code != 200:
            response = requests.get("https://restcountries.com/v3.1/all", timeout=10)
            response.raise_for_status()
            countries_data = response.json()
            code = response.status_code
            time.sleep(.5)
        return countries_data
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Problème lors de la récupération des pays via l'API : {e}")
        return

def get_countries_region_from_json() :
    """
    Charge les données de la région des pays à partir du fichier JSON local.

    Cette fonction ouvre le fichier `pays_region.json` et charge les données JSON qu'il contient.
    Ces données correspondent à la région de chaque pays, qui sera utilisée lors de l'insertion 
    dans la base de données.

    Returns:
        dict or None: Dictionnaire des régions des pays si le fichier est chargé correctement, sinon None.
    """
    try:
        with open(PAYS_REGION_JSON, "r", encoding="utf-8") as file:
            pays_data = json.load(file)
            return pays_data
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Problème lors de la récupération des pays via l'API : {e}")
        return

def fetch_climat_type():
    """
    Récupère les types de climat depuis la base de données.

    Cette fonction interroge la table `climat_type` dans la base de données 
    pour obtenir les ID des types de climat et 
    leurs noms associés. Elle retourne un dictionnaire avec le nom du climat 
    en minuscule comme clé et l'ID comme valeur.

    Returns:
        dict: Dictionnaire des types de climat avec le nom comme clé et l'ID comme valeur.
        dict: Dictionnaire vide en cas d'erreur.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_climat_type, name FROM climat_type;")
        return {row[1].lower(): row[0] for row in cursor.fetchall()}
    except Exception as e:
        print(f"[ERROR] Problème lors de la récupération des ID climat: {e}")
        return {}
    finally:
        cursor.close()
        conn.close()

def set_countries():
    """
    Récupère et insère les données des pays dans la base de données.

    Cette fonction combine plusieurs étapes :
    - Récupère les données des pays via l'API Restcountries.
    - Charge les données de la région des pays à partir d'un fichier JSON.
    - Récupère les informations sur le PIB via l'API Ninjas.
    - Récupère les continents et régions depuis la base de données.
    - Insère les pays et leurs informations dans la table `country` de la base de données.

    En cas d'erreur, des messages d'erreur sont affichés et la transaction est annulée.

    Returns:
        None
    """
    truncate_table("country")

    countries_data = get_countries_from_api()

    country_region = get_countries_region_from_json()

    gdp_map = fetch_gdp_data(API_KEY, GDP_API_URL)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id_continent, name FROM continent;")
        continent_map = {row[1]: row[0] for row in cursor.fetchall()}

        values = []
        for country in countries_data:
            name = country.get("name", {}).get("common", "").strip().lower()
            population = country.get("population")
            continent = country.get("continents", "")[0].strip().lower()
            iso_code = country.get("cca3", "").strip()
            pib = gdp_map.get(iso_code, None)
            latlng = country.get("latlng", [])
            if len(latlng) >= 2:
                latitude = latlng[0]
                longitude = latlng[1]
            else:
                latitude = None
                longitude = None
            region = country_region.get(name.title(), {}).get("region", "").strip().lower()
            cursor.execute("SELECT id_region FROM region WHERE name = %s;", (region,))

            print(f"[INFO] Préparation de l'insertion du pays : {name} (Région: {region})")

            result = cursor.fetchone()
            id_region = result[0] if result else None

            if not name \
                or not population \
                or not continent \
                or not iso_code \
                or not latitude \
                or not longitude \
                or not pib \
                or not id_region \
                or not iso_code:
                continue

            id_continent = continent_map.get(continent.lower())

            if not id_continent:
                print(f"[WARNING] Continent inconnu pour {name} (Continent: {continent})")
                continue

            values.append((name, iso_code, population, id_continent, pib, latitude, longitude, id_region))

        if not values:
            print("[ERROR] Aucun pays valide à insérer.")
            return

        sql = """
            INSERT INTO country (name, iso_code, population, id_continent, pib, latitude, longitude, id_region)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        execute_batch(cursor, sql, values)
        conn.commit()
        print(f"[INFO] {len(values)} pays insérés dans la table 'country'.")

        set_country_climat_types()

    except Exception as e:
        print(f"[ERROR] Problème lors de l'insertion des pays en base : {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
