from src.config import BRONZE_PARQUET_PATH
from src.config import SILVER_PARQUET_PATH
import pandas as pd


def process_silver_orders():

    # Read the Bronze data
    df = pd.read_parquet(
        BRONZE_PARQUET_PATH / "olist_orders_dataset.parquet"
    )

    # Columns containing dates
    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    nulls_before = df[date_columns].isna().sum()
    # Convert the columns to datetime
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Count missing values after conversion
    nulls_after = df[date_columns].isna().sum()

    # Calculate the new missing values
    conversion_errors = nulls_after - nulls_before
    # Display date conversion errors
    print("Erreurs de conversion des dates :")
    print(conversion_errors)

    df["anomalie_livraison"] = (
    (df["order_status"] == "delivered")
    & (df["order_delivered_customer_date"].isna())
)

    delivery_anomalies = df[df["anomalie_livraison"]]

    # Create the Silver directory if it does not exist
    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)

    # Define the Silver file path
    parquet_file = SILVER_PARQUET_PATH / "orders.parquet"

    # Save the cleaned DataFrame
    df.to_parquet(parquet_file, index=False)

    return df

if __name__ == "__main__":
    process_silver_orders()