"""
Module pour récupérer l'identifiant d'un pays basé sur son nom.

Ce module utilise une fonction utilitaire pour convertir le nom d'un pays
en code ISO2, puis recherche cet identifiant dans une structure de données
fournie. Il est utile pour normaliser et associer des informations à des
pays dans des bases de données ou des ensembles de données.

Classes, Fonctions et Modules Importés :
----------------------------------------
- get_country_code_by_name : Fonction utilitaire utilisée pour convertir
  un nom de pays en code ISO2.
"""

from utils.get_country_code_by_name import get_country_code_by_name as get_country_code

def get_country_id(country_name, countries):
    """
    Retourne l'identifiant d'un pays en fonction de son nom.

    Cette fonction prend en entrée le nom d'un pays et un dictionnaire de pays
    (`countries`) où les clés sont des codes ISO2 et les valeurs sont les identifiants.
    Elle convertit le nom du pays en code ISO2, puis retourne l'identifiant
    correspondant s'il est présent dans le dictionnaire. Sinon, elle retourne `None`.

    :param country_name: Nom du pays à convertir.
    :type country_name: str
    :param countries: Dictionnaire des pays où les clés sont des codes ISO2 et
                      les valeurs sont les identifiants associés.
    :type countries: dict
    :return: Identifiant du pays ou `None` si le code ISO2 n'est pas trouvé.
    :rtype: Any
    """
    iso_code = get_country_code(country_name)  # Conversion du nom en code ISO2
    return countries.get(iso_code, None)
