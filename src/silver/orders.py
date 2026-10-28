from src.config import BRONZE_PARQUET_PATH
from src.config import SILVER_PARQUET_PATH
import pandas as pd


def process_silver_orders():

    # Lire les données Bronze
    df = pd.read_parquet(
        BRONZE_PARQUET_PATH / "olist_orders_dataset.parquet"
    )

    # Colonnes contenant des dates
    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    nulls_avant = df[date_columns].isna().sum()
    # Convertir les colonnes en datetime
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Compter les valeurs manquantes après conversion
    nulls_apres = df[date_columns].isna().sum()

    # Calculer les nouvelles valeurs manquantes
    erreurs_conversion = nulls_apres - nulls_avant

    df["anomalie_livraison"] = (
    (df["order_status"] == "delivered")
    & (df["order_delivered_customer_date"].isna())
)

    anomalies_livraison = df[df["anomalie_livraison"]]

    # Créer le dossier Silver s'il n'existe pas
    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)

    # Définir le chemin du fichier Silver
    parquet_file = SILVER_PARQUET_PATH / "orders.parquet"

    # Enregistrer le DataFrame nettoyé
    df.to_parquet(parquet_file, index=False)

    return df

if __name__ == "__main__":
    process_silver_orders()