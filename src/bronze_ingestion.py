from src.config import BRONZE_DATA_PATH, BRONZE_PARQUET_PATH
import pandas as pd


def process_bronze_orders():

    # Path to the CSV files
    raw_path = BRONZE_DATA_PATH 

    # Find all CSV files
    csv_files = sorted(raw_path.glob("*.csv"))

    # Display the number of files found
    print(f"Nombre de fichiers CSV : {len(csv_files)}")

    # Iterate over the files
    for csv_file in csv_files:
        print(csv_file.name)

    BRONZE_PARQUET_PATH.mkdir(parents=True, exist_ok=True)
    
    # Iterate over all CSV files
    for csv_file in csv_files:

        # Read the CSV file
        df = pd.read_csv(csv_file)

        # Build the Parquet file name
        parquet_file = BRONZE_PARQUET_PATH / (
            csv_file.stem + ".parquet"
        )

        # Save the data in Parquet format
        df.to_parquet(parquet_file, index=False)

        # Display the result
        print(f"Fichier : {csv_file.name}")
        print(f"Nombre de lignes : {len(df)}")
        print(f"Parquet créé : {parquet_file}")
        print("----------------------------")


if __name__ == "__main__":
    process_bronze_orders()