"""
Ce module permet de récupérer les données de PIB nominal (en milliards USD) pour l'année 2020 via 
l'API API-Ninjas. La fonction permet de collecter ces données et de les convertir en un dictionnaire, 
où la clé est le code du pays et la valeur est le PIB nominal du pays.
"""

import requests # type: ignore


def fetch_gdp_data(api_key, gdp_api_url):
    """
    Récupère les données de PIB nominal (en milliards USD) pour l'année 2020 depuis l'API API-Ninjas.

    Cette fonction envoie une requête GET à l'API API-Ninjas pour récupérer les données de PIB nominal 
    pour l'année 2020. Si la réponse est valide, les données sont traitées et converties en un dictionnaire 
    avec le code du pays comme clé et le PIB nominal en dollars comme valeur. Les données sont retournées 
    après conversion.

    Si aucune donnée valide n'est récupérée ou en cas d'erreur de requête, la fonction retourne un 
    dictionnaire vide.

    Args:
        api_key (str): Clé d'API nécessaire pour accéder à l'API API-Ninjas.
        gdp_api_url (str): URL de l'API API-Ninjas pour récupérer les données de PIB.

    Returns:
        dict: Dictionnaire contenant les pays comme clés et leur PIB nominal en dollars comme valeurs. 
              Si une erreur se produit, un dictionnaire vide est retourné.
    """
    try:
        print(f"[INFO] Récupération des données de PIB depuis {gdp_api_url}")
        response = requests.get(gdp_api_url, headers={'X-Api-Key': api_key}, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            print("[WARNING] Aucune donnée valide récupérée pour le PIB.")
            return {}

        print(f"[INFO] {len(data)} enregistrements de PIB récupérés.")

        gdp_map = {}
        for entry in data:
            country_code = entry.get("country")
            gdp_nominal = entry.get("gdp_nominal")

            if country_code and gdp_nominal is not None:
                gdp_map[country_code] = gdp_nominal * 1_000_000_000  # Conversion en dollars

        return gdp_map

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Problème lors de la récupération des données du PIB : {e}")
        return {}
