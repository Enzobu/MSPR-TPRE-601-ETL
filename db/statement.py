"""
Module d'insertion de données dans une base de données.

Ce module fournit une fonction pour insérer des données dans une table PostgreSQL à l'aide de Spark. 
Il établit une connexion JDBC à la base de données et insère les données contenues dans un DataFrame Spark.

Fonctionnalités principales :
- Connexion à une base de données PostgreSQL via JDBC.
- Écriture des données d'un DataFrame Spark dans une table spécifique.
- Affichage des données avant insertion pour vérifier leur contenu.

Dépendances :
- Un environnement Spark correctement configuré.
- Une base de données PostgreSQL accessible.
- Le connecteur JDBC PostgreSQL.

"""

from spark.spark import spark_session

def set_statement(df_final):
    """
    Insère les données dans la table 'statement' d'une base de données PostgreSQL.

    Cette fonction effectue les opérations suivantes :
    1. Affiche les 50 premières lignes du DataFrame pour vérifier les données.
    2. Établit une connexion JDBC avec la base de données PostgreSQL.
    3. Insère les données du DataFrame Spark dans la table 'statement' en mode 'append'.
    4. Arrête la session Spark après l'opération.

    Args:
        df_final (pyspark.sql.DataFrame): Le DataFrame Spark contenant les données à insérer.

    Returns:
        None

    Exemple:
        >>> set_statement(df_final)
        +----------+--------+--------+--------+--------+----------+-----------+
        |     _date|Confirmed|  Deaths|Recovered|   Active|id_disease|id_country|
        +----------+--------+--------+--------+--------+----------+-----------+
        |2020-01-22|      444|       17|      28|     399|         1|        10|
        +----------+--------+--------+--------+--------+----------+-----------+
        [INFO] Lignes insérées dans la table 'statement'.

    Exceptions:
        Exception: Si une erreur se produit lors de l'écriture dans la base de données.
    """
    spark = spark_session()
    df_final.show(50)

    jdbc_url = "jdbc:postgresql://qg.enzo-palermo.com:5432/mspr502"
    properties = {
        "user": "mspr502",
        "password": "s5t4v5",
        "driver": "org.postgresql.Driver"
    }

    df_final.write \
        .jdbc(url=jdbc_url, table="statement", mode="append", properties=properties)

    spark.stop()

    print("[INFO] Lignes insérées dans la table 'statement'.")
