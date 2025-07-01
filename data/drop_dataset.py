"""
Module de suppression des ensembles de données.

Ce module fournit une fonction pour supprimer un dossier contenant des ensembles de données. 
Il vérifie si le dossier existe avant de le supprimer, et gère les erreurs potentielles liées 
à l'absence du dossier ou aux permissions insuffisantes.

Fonctionnalités principales :
- Vérification de l'existence d'un dossier spécifique.
- Suppression récursive du dossier et de son contenu.
- Gestion des erreurs et affichage des messages informatifs.

Dépendances :
- Le module `os` pour vérifier l'existence du dossier.
- Le module `shutil` pour la suppression récursive des dossiers.

"""

import os
import shutil


def drop_dataset():
    """
    Supprime le dossier contenant les ensembles de données.

    Cette fonction effectue les opérations suivantes :
    1. Vérifie si le dossier spécifié existe.
    2. Si le dossier existe, le supprime ainsi que tout son contenu.
    3. Si le dossier n'existe pas, lève une erreur `FileNotFoundError`.
    4. Affiche un message d'information en cas de succès ou un message d'erreur en cas d'échec.

    Returns:
        None

    Exceptions:
        FileNotFoundError: Si le dossier spécifié n'existe pas.
        Exception: En cas d'erreur lors de la suppression du dossier.

    Exemple:
        >>> drop_dataset()
        [INFO] Dossier supprimé : ./data_files
    """
    data_folder = "./data_files"

    try:
        if not os.path.exists(data_folder):
            raise FileNotFoundError(f"Le dossier '{data_folder}' n'existe pas.")
        shutil.rmtree(data_folder)
        print(f"[INFO] Dossier supprimé : {data_folder}")
    except Exception as e:
        print(f"[ERROR] {e}")
