from pyspark.sql.functions import col, udf, lit, sum as F_sum   # type: ignore
from pyspark.sql.types import IntegerType, StringType           # type: ignore

from utils.get_country_code_by_name import get_country_code_by_name as get_country_code
from db.connection import get_connection
from spark.spark import spark_session


def clean_covid():
    """
    Nettoie et agrège les données COVID-19 à partir d'un nouveau format.

    Colonnes attendues :
    - Date_reported
    - Country_code
    - Country
    - WHO_region
    - New_cases
    - Cumulative_cases
    - New_deaths
    - Cumulative_deaths

    Returns:
        pyspark.sql.DataFrame: DataFrame PySpark agrégé avec les colonnes :
            - `_date`
            - `id_country`
            - `id_disease`
            - `Confirmed` (cumulative_cases)
            - `Deaths` (cumulative_deaths)
    """
    spark = spark_session()

    df = spark.read.csv(
        # "data_files/corona-virus-report/covid_19_clean_complete.csv",
        "data_files/WHO-COVID-19-global-daily-data.csv",
        header=True,
        inferSchema=True
    )

    df = df.repartition(6)
    print(f"Nombre de partitions : {df.rdd.getNumPartitions()}")

    # Connexion base de données
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
        on="iso_code",
        how="left"
    )

    # Récupération ID maladie
    cursor.execute("SELECT id_disease FROM disease WHERE name = 'covid'")
    id_disease = cursor.fetchone()[0]

    df = df.withColumn("id_disease", lit(id_disease).cast(IntegerType()))

    df = df.select(
        col("Date_reported").alias("_date"),
        col("Cumulative_cases").cast(IntegerType()).alias("Confirmed"),
        col("Cumulative_deaths").cast(IntegerType()).alias("Deaths"),
        col("id_country"),
        col("id_disease")
    ).dropna()

    # Agrégation si besoin (même si souvent les données sont déjà au niveau agrégé)
    df_aggregated = df.groupBy("_date", "id_country", "id_disease").agg(
        F_sum("Confirmed").alias("Confirmed"),
        F_sum("Deaths").alias("Deaths")
    )

    cursor.close()
    conn.close()

    return df_aggregated