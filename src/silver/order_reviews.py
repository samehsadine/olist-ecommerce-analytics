import pandas as pd
from src.config import BRONZE_PARQUET_PATH, SILVER_PARQUET_PATH


def process_silver_order_reviews():

    # 1. Read the Bronze data
    df_reviews = pd.read_parquet(
        BRONZE_PARQUET_PATH / "olist_order_reviews_dataset.parquet"
    )

    # 2. Convert the dates
    date_columns = [
        "review_creation_date",
        "review_answer_timestamp"
    ]

    for column in date_columns:
        df_reviews[column] = pd.to_datetime(
            df_reviews[column],
            errors="coerce"
        )

    SILVER_PARQUET_PATH.mkdir(parents=True, exist_ok=True)

    # 7. Save the Silver file
    parquet_file = SILVER_PARQUET_PATH / "order_reviews.parquet"

    df_reviews.to_parquet(parquet_file, index=False)

    print(f"Fichier Silver enregistré : {parquet_file}")
    print(f"Nombre de lignes : {len(df_reviews)}")

    return df_reviews


if __name__ == "__main__":
    process_silver_order_reviews()