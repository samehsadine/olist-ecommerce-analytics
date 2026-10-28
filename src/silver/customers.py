from src.config import BRONZE_PARQUET_PATH
from src.config import SILVER_PARQUET_PATH
import pandas as pd


def process_silver_customers():

    df_customers = pd.read_parquet(
        BRONZE_PARQUET_PATH / "olist_customers_dataset.parquet"
    )

    df_customers["customer_zip_code_prefix"] = (
        df_customers["customer_zip_code_prefix"]
        .astype("string")
        .str.zfill(5)
    )

    if df_customers["customer_id"].duplicated().any():
        raise ValueError("Des customer_id sont dupliqués.")

    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)

    # 5. Enregistrer les données nettoyées
    parquet_file = SILVER_PARQUET_PATH / "customers.parquet"

    df_customers.to_parquet(parquet_file, index=False)

    print(f"Customers Silver enregistré : {len(df_customers)} lignes")

    return df_customers


if __name__ == "__main__":
    process_silver_customers()
