from src.config import BRONZE_PARQUET_PATH
from src.config import SILVER_PARQUET_PATH
import pandas as pd

def process_silver_geolocation():

    df_geolocation= pd.read_parquet(
            BRONZE_PARQUET_PATH / "olist_geolocation_dataset.parquet"
    )

    # Convert the postal code to a 5-character string
    df_geolocation["geolocation_zip_code_prefix"] = (
    df_geolocation["geolocation_zip_code_prefix"]
    .astype("string")
    .str.zfill(5)
    )

    rows_before = len(df_geolocation)
    df_geolocation = df_geolocation.drop_duplicates()
    rows_after = len(df_geolocation)

    duplicates_removed = rows_before - rows_after

    print("Doublons supprimés :", duplicates_removed)
    print("Nombre de lignes restantes :", rows_after)

    df_geolocation["anomalie_geolocation"] = (
    ~df_geolocation["geolocation_lat"].between(-34, 6)
    |
    ~df_geolocation["geolocation_lng"].between(-74, -34)
)

# Count suspicious coordinates
    print(
        "Coordonnées suspectes :",
        df_geolocation["anomalie_geolocation"].sum()
    )

    # Create the Silver directory if it does not exist
    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)

    # Define the Silver file path
    parquet_file = SILVER_PARQUET_PATH / "geolocation.parquet"

    # Save the cleaned data
    df_geolocation.to_parquet(parquet_file, index=False)

    print(f"Fichier Silver enregistré : {parquet_file}")
    print(f"Nombre de lignes : {len(df_geolocation)}")

if __name__ == "__main__":
    process_silver_geolocation()