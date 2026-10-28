from src.config import BRONZE_PARQUET_PATH
from src.config import SILVER_PARQUET_PATH
import pandas as pd

def process_silver_geolocation():

    df_geolocation= pd.read_parquet(
            BRONZE_PARQUET_PATH / "olist_geolocation_dataset.parquet"
    )

    # Convertir le code postal en chaîne de 5 caractères
    df_geolocation["geolocation_zip_code_prefix"] = (
    df_geolocation["geolocation_zip_code_prefix"]
    .astype("string")
    .str.zfill(5)
    )

    lignes_avant = len(df_geolocation)
    df_geolocation = df_geolocation.drop_duplicates()
    lignes_apres = len(df_geolocation)

    doublons_supprimes = lignes_avant - lignes_apres

    print("Doublons supprimés :", doublons_supprimes)
    print("Nombre de lignes restantes :", lignes_apres)

    df_geolocation["anomalie_geolocation"] = (
    ~df_geolocation["geolocation_lat"].between(-34, 6)
    |
    ~df_geolocation["geolocation_lng"].between(-74, -34)
)

# Compter les coordonnées suspectes
    print(
        "Coordonnées suspectes :",
        df_geolocation["anomalie_geolocation"].sum()
    )

    # Créer le dossier Silver s'il n'existe pas
    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)

    # Définir le chemin du fichier Silver
    parquet_file = SILVER_PARQUET_PATH / "geolocation.parquet"

    # Enregistrer les données nettoyées
    df_geolocation.to_parquet(parquet_file, index=False)

    print(f"Fichier Silver enregistré : {parquet_file}")
    print(f"Nombre de lignes : {len(df_geolocation)}")

if __name__ == "__main__":
    process_silver_geolocation()