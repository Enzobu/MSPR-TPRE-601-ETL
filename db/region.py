"""
Ce module est responsable de l'extraction et de l'insertion des données de régions dans la base de données.
Il utilise Spark pour lire un fichier JSON, extraire les régions et les insérer dans la table `region` 
de la base de données.
"""

from pyspark.sql.functions import col   # type: ignore
from spark.spark import spark_session
from db.connection import get_connection
from db.truncate_table import truncate_table


def get_region():
    """
    Récupère la liste des régions à partir d'un fichier JSON et les retourne sous forme de liste.

    Cette fonction utilise Spark pour lire un fichier JSON contenant des données sur les pays et leurs régions. 
    Les régions sont extraites, dédupliquées et retournées sous forme d'une liste.

    Utilise Apache Spark pour le traitement des données en DataFrame et la gestion des données volumineuses.

    Returns:
        list: Liste des régions extraites du fichier JSON. Les régions sont uniques et non nulles.
    """
    spark = spark_session()

    json_file_path = "./json/pays_region.json"
    df = spark.read.option("multiline", "true").json(json_file_path)

    regions_list = []

    for country in df.columns:
        country_region = df.select(col(country).getItem("region").alias("region"))
        regions_list.append(country_region)

    regions_df = regions_list[0]
    for region in regions_list[1:]:
        regions_df = regions_df.union(region)

    regions_df = regions_df.dropDuplicates()

    regions_list = [row["region"] for row in regions_df.collect() if row["region"]]

    spark.stop()

    return regions_list


def set_region():
    """
    Insère les régions extraites dans la base de données.

    Cette fonction récupère les régions via la fonction `get_region()`, vide la table `region` avec 
    la fonction `truncate_table` et insère ensuite chaque région dans la table `region` de la base de données.

    Returns:
        None
    """
    conn = get_connection()
    cursor = conn.cursor()

    truncate_table("region")

    regions_list = get_region()

    for region in regions_list:
        region = region.lower()
        cursor.execute("""
            INSERT INTO region (name) 
            VALUES (%s) 
        """, (region,))
        print(f"[INFO] Région insérée : {region}")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    set_region()
