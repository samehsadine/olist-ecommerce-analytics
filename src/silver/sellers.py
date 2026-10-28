from src.config import BRONZE_PARQUET_PATH
from src.config import SILVER_PARQUET_PATH
import pandas as pd

def process_silver_sellers():

    df_sellers = pd.read_parquet(
            BRONZE_PARQUET_PATH / "olist_sellers_dataset.parquet"
    )

    # Convertir le code postal en chaîne de 5 caractères
    df_sellers["seller_zip_code_prefix"] = (
    df_sellers["seller_zip_code_prefix"]
    .astype("string")
    .str.zfill(5)
    )
    # Créer le dossier Silver s'il n'existe pas
    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)

    # Définir le chemin du fichier Silver
    parquet_file = SILVER_PARQUET_PATH / "sellers.parquet"

    # Enregistrer le DataFrame nettoyé
    df_sellers.to_parquet(parquet_file, index=False)


    print(f"Fichier Silver enregistré : {parquet_file}")
    print(f"Nombre de lignes : {len(df_sellers)}")
    print(df_sellers.dtypes)

    return df_sellers


if __name__ == "__main__":
    process_silver_sellers()