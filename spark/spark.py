"""
Module pour initialiser une session Spark.

Ce module contient une fonction permettant de configurer et de démarrer
une session Spark, qui peut être utilisée pour effectuer des opérations
de traitement et de nettoyage de données volumineuses.

Classes, Fonctions et Modules Importés :
----------------------------------------
- pyspark.sql.SparkSession : Fournit des fonctionnalités pour gérer une
  session Spark.
"""

from pyspark.sql import SparkSession   # type: ignore

def spark_session():
    """
    Initialise et retourne une session Spark.

    Cette fonction configure une session Spark en lui attribuant un nom d'application
    ("DataCleaning") et retourne une instance de SparkSession. Elle peut être utilisée
    pour charger, transformer et analyser des données avec Spark.

    :return: Une instance de SparkSession configurée.
    :rtype: pyspark.sql.SparkSession
    """
    return SparkSession.builder \
        .appName("DataCleaning") \
        .getOrCreate()
