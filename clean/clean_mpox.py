"""
Module de nettoyage des données pour la variole du singe (Monkeypox).

Ce module utilise PySpark pour nettoyer et transformer les données brutes concernant la variole du singe. 
Les données sont enrichies avec des informations sur les pays, associées à l'identifiant de la maladie, 
et agrégées par date, pays et maladie avant d'être prêtes à être insérées dans une base de données.

Fonctionnalités principales :
- Chargement et partitionnement des données brutes.
- Enrichissement des données avec des identifiants de pays issus d'une base de données.
- Association des données à l'identifiant de la maladie.
- Agrégation des cas et décès cumulés.
- Gestion des valeurs manquantes et transformation des colonnes.

Dépendances :
- PySpark pour le traitement et l'agrégation des données.
- Une base de données pour récupérer les informations sur les pays et les maladies.
- Un fichier CSV contenant les données brutes sur la variole du singe.

"""

from pyspark.sql.functions import udf, lit, col, sum as F_sum   # type: ignore
from pyspark.sql.types import IntegerType                       # type: ignore
from pyspark.sql.types import StringType                        # type: ignore

from db.connection import get_connection
from spark.spark import spark_session
from utils.get_country_code_by_name import get_country_code_by_name as get_country_code


def clean_mpox():
    """
    Nettoie et transforme les données brutes sur la variole du singe (Monkeypox).

    Cette fonction effectue les opérations suivantes :
    1. Chargement des données brutes depuis un fichier CSV.
    2. Partitionnement des données pour optimiser leur traitement avec PySpark.
    3. Enrichissement des données avec les identifiants des pays via une base de données.
    4. Association des données à l'identifiant de la maladie Monkeypox.
    5. Agrégation des cas et des décès cumulés par date, pays et maladie.
    6. Gestion des valeurs manquantes et suppression des colonnes inutiles.

    Returns:
        pyspark.sql.DataFrame: Un DataFrame PySpark contenant les données nettoyées, enrichies et agrégées, 
        prêtes pour l'insertion dans une base de données.

    Exceptions:
        Lève des erreurs en cas de problème avec la connexion à la base de données ou le traitement des données.
    """
    spark = spark_session()

    df = spark.read.csv(
        "data_files/mpox-monkeypox-data/owid-monkeypox-data.csv", 
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

    df = df.withColumn("iso_code", get_country_code_udf(col("`location`")))

    df = df.join(
        countries_df,
        df["iso_code"] == countries_df["iso_code"],
        how="left"
    ).drop("iso_code")

    cursor.execute("SELECT id_disease FROM disease WHERE name = 'monkeypox'")
    id_disease = cursor.fetchone()[0]

    df = df.withColumn("id_disease", lit(id_disease).cast(IntegerType()))

    df = df.select(
        col("date").alias("_date"),
        col("total_cases").cast(IntegerType()),
        col("total_deaths").cast(IntegerType()),
        col("id_disease"),
        col("id_country")
    ).dropna()

    df_aggregated = df.groupBy(
        "_date", "id_country", "id_disease"
    ).agg(
        F_sum("total_cases").alias("Confirmed"),
        F_sum("total_deaths").alias("Deaths"),
    )

    cursor.close()
    conn.close()

    return df_aggregated
