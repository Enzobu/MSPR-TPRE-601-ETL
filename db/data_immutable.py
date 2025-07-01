"""
Ce module est responsable de l'insertion des données immuables dans la base de données, telles que les types 
de climat,les continents, les régions et les pays. Il appelle différentes fonctions pour insérer les données 
dans les tables correspondantes de la base de données dans un ordre spécifique.
"""

from db.countries import set_countries
from db.continents import set_continents
from db.climat_type import set_climat_type
from db.region import set_region


def set_data_immutable():
    """
    Insère les données immuables dans les tables de la base de données.

    Cette fonction appelle plusieurs sous-fonctions pour insérer les données dans les tables `climat_type`, 
    `continent`, `region` et `country` :
    - Insère les types de climat avec la fonction `set_climat_type()`.
    - Insère les continents avec la fonction `set_continents()`.
    - Insère les régions avec la fonction `set_region()`.
    - Insère les pays avec la fonction `set_countries()`.

    Cette fonction assure l'ordre des insertions pour garantir l'intégrité des données.

    Returns:
        None
    """
    print("\n ===== Insertion des données dans climat_type ===== ")
    set_climat_type()

    print("\n ===== Insertion des données dans continent ===== ")
    set_continents()

    print("\n ===== Insertion des données dans region ===== ")
    set_region()

    print("\n ===== Insertion des données dans country ===== ")
    set_countries()
