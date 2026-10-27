from config import ACCESS_DONNEES_PATH, BRONZE_PARQUET_PATH
import pandas as pd


def process_bronze_orders():

    # Chemin vers les fichiers CSV
    raw_path = ACCESS_DONNEES_PATH 

    # Rechercher tous les fichiers CSV
    csv_files = sorted(raw_path.glob("*.csv"))

    # Afficher le nombre de fichiers trouvés
    print(f"Nombre de fichiers CSV : {len(csv_files)}")

    # Parcourir les fichiers
    for csv_file in csv_files:
        print(csv_file.name)

    BRONZE_PARQUET_PATH.mkdir(parents=True, exist_ok=True)
    
    # Parcourir tous les fichiers CSV
    for csv_file in csv_files:

        # Lire le fichier CSV
        df = pd.read_csv(csv_file)

        # Construire le nom du fichier Parquet
        parquet_file = BRONZE_PARQUET_PATH / (
            csv_file.stem + ".parquet"
        )

        # Enregistrer les données en Parquet
        df.to_parquet(parquet_file, index=False)

        # Afficher le résultat
        print(f"Fichier : {csv_file.name}")
        print(f"Nombre de lignes : {len(df)}")
        print(f"Parquet créé : {parquet_file}")
        print("----------------------------")


if __name__ == "__main__":
    process_bronze_orders()