from src.config import BRONZE_PARQUET_PATH
from src.config import SILVER_PARQUET_PATH
import pandas as pd

def process_silver_orders_items():

    df_orders_items =pd.read_parquet(BRONZE_PARQUET_PATH/"olist_order_items_dataset.parquet")

    shipping_limit_date = df_orders_items["shipping_limit_date"]

    nulls_before = shipping_limit_date.isna().sum()
    # Convert the columns to datetime

    shipping_limit_date = pd.to_datetime(shipping_limit_date, errors="coerce")

    # Count missing values after conversion
    nulls_after = shipping_limit_date.isna().sum()

    # Calculate the new missing values
    conversion_errors = nulls_after - nulls_before

    df_orders_items["shipping_limit_date"] = shipping_limit_date

    print("Erreurs de conversion :", conversion_errors)

    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)

    # Define the Silver file path
    parquet_file = SILVER_PARQUET_PATH / "orders_items.parquet"

    # Save the cleaned DataFrame
    df_orders_items.to_parquet(parquet_file, index=False)

    print(f"Fichier Silver enregistré : {parquet_file}")
    print(f"Nombre de lignes : {len(df_orders_items)}")

    
if __name__ == "__main__":
    process_silver_orders_items()