"""
Ce module récupère des données brutes, insère des données fixes dans les tables appropriées et 
effectue un nettoyage des données avant de les insérer dans une table finale.

Le processus commence par la récupération des données brutes, suivi de l'insertion des données 
fixes liées aux maladies dans la table `disease`. Ensuite, des données fixes sont insérées dans 
les tables appropriées, avant de nettoyer et insérer les données dans la table `statement`.
"""

from datetime import datetime

from data.get_brut_data import get_brut_data
from db.disease import set_disease
from db.data_immutable import set_data_immutable
from clean.clean_data import clean_data
from data.drop_dataset import drop_dataset


# time.sleep(10) # ATENTION : À SUPPRIMER (délais le temps que les containers nécessaires au traitement se montent)

print("======================================================================================")
print("======================================================================================")
print(f"===================== DATE ET HEURE : {datetime.now()} =====================")
print("======================================================================================")
print("======================================================================================")

print("\n\n")
print(" __  __  _____ _____  _____    _____  ___  __ ")
print("|  \/  |/ ____|  __ \|  __ \  | ____|/ _ \/_ |")
print("| \  / | (___ | |__) | |__) | | |__ | | | || |")
print("| |\/| |\___ \|  ___/|  _  /  |___ \| | | || |")
print("| |  | |____) | |    | | \ \   ___) | |_| || |")
print("|_|  |_|_____/|_|    |_|  \_\ |____/ \___/ |_|")
print("\n\n")

print("\n\n ========== Début de la récupération des datas brutes ========== ")
get_brut_data()

# print("\n\n ========== Insertion des données dans disease ========== ")
# set_disease()

# print("\n\n ========== Insertion des données fixes dans les tables ========== ")
# set_data_immutable()

print("\n\n ========== Nettoyage et insertion des données dans statement ========== ")
clean_data()

print("\n\n ========== Suppression des datasets ========== ")
drop_dataset()

print("======================================================================================")
print("======================================================================================")
print(f"===================== DATE ET HEURE : {datetime.now()} =====================")
print("======================================================================================")
print("======================================================================================")