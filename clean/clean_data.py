"""
Module de nettoyage et de préparation des données épidémiologiques.

Ce module orchestre le nettoyage et la transformation des données pour différentes maladies, 
notamment COVID-19, H1N1, MPOX et SRAS, en utilisant PySpark. Après transformation, les données 
sont insérées dans une base de données.

Fonctionnalités principales :
- Appel des fonctions de nettoyage pour chaque maladie.
- Gestion centralisée des erreurs pour chaque étape.
- Troncature préalable des tables cibles pour un traitement propre.
- Insertion des données nettoyées et agrégées dans la table `statement`.

Dépendances :
- PySpark pour le traitement des données.
- Une base de données relationnelle pour stocker les données nettoyées.
- Modules spécifiques pour chaque maladie : `clean_covid`, `clean_h1n1`, `clean_mpox`, et `clean_sras`.

"""

from spark.spark import spark_session
from db.statement import set_statement
from clean.clean_covid import clean_covid
from clean.clean_h1n1 import clean_h1n1
from clean.clean_mpox import clean_mpox
from clean.clean_sras import clean_sras
from db.truncate_table import truncate_table

def clean_data():
    """
    Orchestrateur du nettoyage des données épidémiologiques.

    Cette fonction nettoie, transforme et insère dans une base de données les données 
    relatives à plusieurs maladies (COVID-19, H1N1, MPOX, SRAS). Elle :
    1. Initialise une session PySpark.
    2. Tronque la table `statement` pour éviter les doublons.
    3. Appelle les fonctions de nettoyage et de transformation pour chaque maladie.
    4. Insère les données nettoyées dans la base de données via `set_statement`.
    5. Gère les erreurs individuellement pour chaque maladie, afin de ne pas interrompre 
       le processus en cas de problème.

    Étapes par maladie :
    - Nettoyage des données avec la fonction spécifique (par exemple, `clean_covid`).
    - Insertion dans la table `statement` après transformation.

    Exceptions :
    - Les erreurs lors de l'insertion ou du nettoyage d'une maladie sont affichées dans la console, 
      mais n'arrêtent pas le processus global.

    Returns:
        None
    """
    spark = spark_session()
    truncate_table("statement")

    print("\n ===== Nettoyage des données pour covid ===== ")
    df = clean_covid()
    try:
        set_statement(df)
    except Exception as exception:
        print(f"[ERROR] Une erreur s'est produite pour : covid. {exception}")

    # print("\n ===== Nettoyage des données pour h1n1 ===== ")
    # df = clean_h1n1()
    # try:
    #     set_statement(df)
    # except Exception as exception:
    #     print(f"[ERROR] Une erreur s'est produite pour : h1n1. {exception}")

    # print("\n ===== Nettoyage des données pour mpox ===== ")
    # df = clean_mpox()
    # try:
    #     set_statement(df)
    # except Exception as exception:
    #     print(f"[ERROR] Une erreur s'est produite pour : mpox. {exception}")

    # print("\n ===== Nettoyage des données pour sras ===== ")
    # df = clean_sras()
    # try:
    #     set_statement(df)
    # except Exception as exception:
    #     print(f"[ERROR] Une erreur s'est produite pour : sras. {exception}")

    spark.stop()
