from pathlib import Path

# Chemin racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Chemins des données
ACCESS_DONNEES_PATH = PROJECT_ROOT / "data" / "bronze"
SILVER_PATH = PROJECT_ROOT / "data" / "silver"
GOLD_PATH = PROJECT_ROOT / "data" / "gold"

ACCESS_DONNEES_PATH_SILVER = PROJECT_ROOT / "data" / "silver"


BRONZE_PARQUET_PATH = ACCESS_DONNEES_PATH / "parquet"
SILVER_PARQUET_PATH = ACCESS_DONNEES_PATH_SILVER / "parquet"

#bd
SQL_SERVER = "localhost"
SQL_DATABASE = "OlistAnalytics"
SQL_DRIVER = "ODBC Driver 17 for SQL Server"

SQL_PATH = PROJECT_ROOT   / "sql"  / "01_create_database.sql"