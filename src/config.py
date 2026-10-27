from pathlib import Path

# Chemin racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Chemins des données
ACCESS_DONNEES_PATH = PROJECT_ROOT / "data" / "bronze"
SILVER_PATH = PROJECT_ROOT / "data" / "silver"
GOLD_PATH = PROJECT_ROOT / "data" / "gold"


BRONZE_PARQUET_PATH = ACCESS_DONNEES_PATH / "parquet"