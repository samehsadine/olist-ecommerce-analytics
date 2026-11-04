from src.config import BRONZE_PARQUET_PATH
from src.config import SILVER_PARQUET_PATH
import pandas as pd


def process_silver_orders_payments():

    df_payments = pd.read_parquet(
        BRONZE_PARQUET_PATH / "olist_order_payments_dataset.parquet"
       )

    # Check missing payment values
    missing_payments = df_payments["payment_value"].isna().sum()

    # Check negative payment values
    negative_payments = (df_payments["payment_value"] < 0).sum()

    # Check zero payment values
    zero_payments = (df_payments["payment_value"] == 0).sum()
 
       # Display payment quality checks
    print("Montants manquants :", missing_payments)
    print("Montants négatifs :", negative_payments)
    print("Montants égaux à zéro :", zero_payments)
    # Flag missing, negative or zero payment values

    df_payments["anomalie_montant"] = (
        df_payments["payment_value"].isna()
        | (df_payments["payment_value"] < 0)
        | (df_payments["payment_value"] == 0)
    )
    

    # Flag zero installments
    df_payments["anomalie_versement"] = (
            df_payments["payment_installments"] == 0
        )
    
        # Flag undefined payment methods
    df_payments["anomalie_type_paiement"] = (
            df_payments["payment_type"] == "not_defined"
        )

            # Create the Silver directory if it does not exist
    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)

    # Define the Silver file path
    parquet_file = SILVER_PARQUET_PATH / "orders_payments.parquet"


    # Save the cleaned DataFrame
    df_payments.to_parquet(parquet_file, index=False)
    
    print(f"Fichier silver enregistré: {parquet_file}")
    print(f"Nombre de lignes : {len(df_payments)}")
   

    return df_payments

if __name__ == "__main__":
    process_silver_orders_payments()
