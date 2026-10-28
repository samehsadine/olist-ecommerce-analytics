from src.config import BRONZE_PARQUET_PATH
from src.config import SILVER_PARQUET_PATH
import pandas as pd

def process_silver_orders_items():

    df_orders_items =pd.read_parquet(BRONZE_PARQUET_PATH/"olist_order_items_dataset.parquet")

    shipping_limit_date = df_orders_items["shipping_limit_date"]

    nulls_avant = shipping_limit_date.isna().sum()
    # Convertir les colonnes en datetime

    shipping_limit_date = pd.to_datetime(shipping_limit_date, errors="coerce")

    # Compter les valeurs manquantes après conversion
    nulls_apres = shipping_limit_date.isna().sum()

    # Calculer les nouvelles valeurs manquantes
    erreurs_conversion = nulls_apres - nulls_avant

    df_orders_items["shipping_limit_date"] = shipping_limit_date

    print("Erreurs de conversion :", erreurs_conversion)

    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)

    # Définir le chemin du fichier Silver
    parquet_file = SILVER_PARQUET_PATH / "orders_items.parquet"

    # Enregistrer le DataFrame nettoyé
    df_orders_items.to_parquet(parquet_file, index=False)

    print(f"Fichier Silver enregistré : {parquet_file}")
    print(f"Nombre de lignes : {len(df_orders_items)}")

    
if __name__ == "__main__":
    process_silver_orders_items()