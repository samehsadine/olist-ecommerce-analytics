from src.config import BRONZE_PARQUET_PATH
from src.config import SILVER_PARQUET_PATH
import pandas as pd


def process_silver_orders_payments():

    df_payments = pd.read_parquet(
        BRONZE_PARQUET_PATH / "olist_order_payments_dataset.parquet"
       )
    df_payments["anomalie_montant"] = (
        df_payments["payment_value"] == 0
    )
    
    # Signaler les versements à zéro
    df_payments["anomalie_versement"] = (
            df_payments["payment_installments"] == 0
        )
    
        # Signaler les moyens de paiement non définis
    df_payments["anomalie_type_paiement"] = (
            df_payments["payment_type"] == "not_defined"
        )

            # Créer le dossier Silver s'il n'existe pas
    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)

    # Définir le chemin du fichier Silver
    parquet_file = SILVER_PARQUET_PATH / "orders_payments.parquet"


    # Enregistrer le DataFrame nettoyé
    df_payments.to_parquet(parquet_file, index=False)
    
    print(f"Fichier silver enregistré: {parquet_file}")
    print(f"Nombre de lignes : {len(df_payments)}")
   

    return df_payments

if __name__ == "__main__":
    process_silver_orders_payments()
