from src.config import BRONZE_PARQUET_PATH
from src.config import SILVER_PARQUET_PATH
import pandas as pd

def process_silver_products():

    df_products = pd.read_parquet (BRONZE_PARQUET_PATH/"olist_products_dataset.parquet")

   # Detect missing, zero or negative weights
    df_products["anomalies_poids"] = (
        df_products["product_weight_g"].isna()
        | (df_products["product_weight_g"] == 0)
        | (df_products["product_weight_g"] < 0)
    )

    df_products["anomalies_categorie"] =  ( df_products["product_category_name" ]
                                           .fillna("")
                                           .str.strip()
                                           .eq(""))

        # Create the Silver directory if it does not exist
    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)

    # Define the Silver file path
    parquet_file = SILVER_PARQUET_PATH / "products.parquet"

    # Save the cleaned DataFrame
    df_products.to_parquet(parquet_file, index=False)


    print(f"Fichier Silver enregistré : {parquet_file}")
    print(f"Nombre de lignes : {len(df_products)}")
    print(df_products.dtypes)

    return df_products

if __name__ == "__main__":
    process_silver_products()