from src.config import BRONZE_PARQUET_PATH
from src.config import SILVER_PARQUET_PATH
import pandas as pd

def process_silver_product_category_translate_name():

    df_cat_translate_name= pd.read_parquet(
            BRONZE_PARQUET_PATH / "product_category_name_translation.parquet"
    )

    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)
    
        # Define the Silver file path
    parquet_file = SILVER_PARQUET_PATH / "product_category_translate_name.parquet"
    
        # Save the cleaned DataFrame
    df_cat_translate_name.to_parquet(parquet_file, index=False)
    
    
    print(f"Fichier Silver enregistré : {parquet_file}")
    print(f"Nombre de lignes : {len(df_cat_translate_name)}")
    print(df_cat_translate_name.dtypes)
    
    return df_cat_translate_name
    
    
if __name__ == "__main__":
        process_silver_product_category_translate_name()