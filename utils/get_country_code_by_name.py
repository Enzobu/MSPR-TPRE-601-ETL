"""
Module pour convertir le nom d'un pays en son code ISO3.

Ce module utilise la bibliothèque `country_converter` pour convertir
les noms de pays en codes ISO3. Cela peut être utile pour normaliser
les données géographiques ou pour effectuer des analyses basées sur
les codes standardisés des pays.

Classes, Fonctions et Modules Importés :
----------------------------------------
- country_converter : Bibliothèque utilisée pour convertir les noms
  de pays en différents formats, y compris les codes ISO3.
"""

import country_converter as coco # type: ignore

def get_country_code_by_name(country_name):
    """
    Convertit le nom d'un pays en code ISO3.

    Cette fonction prend en entrée un nom de pays sous forme de chaîne,
    le convertit en code ISO3 à l'aide de la bibliothèque `country_converter`,
    et retourne le code résultant. Si le nom du pays est invalide ou si
    aucune correspondance n'est trouvée, la fonction retourne `None`.

    :param country_name: Nom du pays à convertir.
    :type country_name: str
    :return: Code ISO3 du pays ou `None` si la conversion échoue.
    :rtype: str ou None
    """
    iso_code = coco.convert(names=country_name.lower(), to="ISO3")
    return iso_code \
        if isinstance(iso_code, str) \
        else iso_code[0] \
        if isinstance(iso_code, list) and iso_code \
        else None
