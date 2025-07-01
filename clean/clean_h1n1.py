"""
Module de nettoyage des données pour la pandémie de grippe H1N1 de 2009.

Ce module utilise PySpark pour nettoyer et transformer les données brutes sur la pandémie de grippe H1N1. 
Les données sont enrichies avec des informations sur les pays, agrégées, et associées à une maladie 
spécifique avant d'être prêtes à être insérées dans une base de données.

Fonctionnalités principales :
- Chargement et partitionnement des données brutes.
- Enrichissement des données avec les informations sur les pays à partir d'une base de données.
- Association des données à l'identifiant de la maladie H1N1.
- Agrégation des cas et décès cumulés par date, pays et maladie.
- Gestion des valeurs manquantes et suppression des colonnes inutiles.

Dépendances :
- PySpark pour le traitement et l'agrégation des données.
- Une base de données pour récupérer les informations sur les pays et les maladies.
- Un fichier CSV contenant les données brutes sur H1N1.

"""

from pyspark.sql.functions import udf, lit, col, sum as F_sum   # type: ignore
from pyspark.sql.types import IntegerType                       # type: ignore
from pyspark.sql.types import StringType                        # type: ignore

from utils.get_country_code_by_name import get_country_code_by_name as get_country_code
from db.connection import get_connection
from spark.spark import spark_session


def clean_h1n1():
    """
    Nettoie et transforme les données brutes sur la pandémie de grippe H1N1.

    Cette fonction effectue les opérations suivantes :
    1. Chargement des données brutes à partir d'un fichier CSV.
    2. Partitionnement des données pour optimiser le traitement avec PySpark.
    3. Enrichissement des données avec les identifiants des pays depuis une base de données.
    4. Association des données à l'identifiant de la maladie H1N1.
    5. Agrégation des cas et décès cumulés par date, pays et maladie.
    6. Gestion des valeurs manquantes pour garantir la qualité des données finales.

    Returns:
        pyspark.sql.DataFrame: Un DataFrame PySpark contenant les données nettoyées, enrichies et agrégées, 
        prêtes pour l'insertion dans une base de données.

    Exceptions:
        Lève des erreurs si des problèmes surviennent lors de l'accès à la base de données ou du traitement
        des données.
    """
    spark = spark_session()

    df = spark.read.csv(
        "data_files/h1n1-swine-flu-2009-pandemic-dataset/data.csv", 
        header=True,
        inferSchema=True
    )

    df = df.repartition(6)
    print(df.rdd.getNumPartitions())

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_country, iso_code FROM country")
    countries = {iso_code: id_country for id_country, iso_code in cursor.fetchall()}

    countries_data = [(id_country, iso_code) for iso_code, id_country in countries.items()]
    countries_columns = ["id_country", "iso_code"]
    countries_df = spark.createDataFrame(countries_data, countries_columns)

    @udf(StringType())
    def get_country_code_udf(country_name):
        return get_country_code(country_name) if country_name else None

    df = df.withColumn("iso_code", get_country_code_udf(col("`Country`")))

    df = df.join(
        countries_df,
        df["iso_code"] == countries_df["iso_code"],
        how="left"
    ).drop("iso_code")

    cursor.execute("SELECT id_disease FROM disease WHERE name = 'h1n1'")
    id_disease = cursor.fetchone()[0]

    df = df.withColumn("id_disease", lit(id_disease).cast(IntegerType()))

    df_final = df.select(
        col("Date").alias("_date"),
        col("`Cumulative no. of cases`").alias("Confirmed"),
        col("`Cumulative no. of deaths`").alias("Deaths"),
        col("id_disease"),
        col("id_country")
    ).dropna()

    df_aggregated = df_final.groupBy(
        "_date", "id_country", "id_disease"
    ).agg(
        F_sum("Confirmed").alias("Confirmed"),
        F_sum("Deaths").alias("Deaths")
    )

    cursor.close()
    conn.close()

    return df_aggregated
