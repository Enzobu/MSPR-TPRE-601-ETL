"""
Ce module fournit une fonction pour vider une table de la base de données et réinitialiser ses identifiants.
La fonction utilise une requête SQL `TRUNCATE` pour effacer toutes les données de la table et réinitialiser 
ses identifiants.
"""

from db.connection import get_connection


def truncate_table(table):
    """
    Vide la table spécifiée et réinitialise les identifiants.

    Cette fonction exécute une requête SQL `TRUNCATE` pour supprimer toutes les lignes de la table spécifiée 
    et réinitialiser les identifiants (généralement utilisés pour les colonnes `SERIAL` ou `BIGSERIAL`), 
    ce qui permet de redémarrer les valeurs des identifiants à partir de 1. L'option `CASCADE` garantit 
    que les relations de clé étrangère sont prises en compte.

    Args:
        table (str): Le nom de la table à vider.

    Returns:
        None
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"

    cursor.execute(sql)
    conn.commit()

    print(f"[INFO] Table {table} vidée.")

    cursor.close()
    conn.close()
