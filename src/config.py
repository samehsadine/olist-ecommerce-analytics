from pathlib import Path

# Project root path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data paths
BRONZE_DATA_PATH = PROJECT_ROOT / "data" / "bronze"
SILVER_PATH = PROJECT_ROOT / "data" / "silver"
GOLD_PATH = PROJECT_ROOT / "data" / "gold"

SILVER_DATA_PATH = PROJECT_ROOT / "data" / "silver"


BRONZE_PARQUET_PATH = BRONZE_DATA_PATH / "parquet"
SILVER_PARQUET_PATH = SILVER_DATA_PATH / "parquet"

# Database
SQL_SERVER = "localhost"
SQL_DATABASE = "OlistAnalytics"
SQL_DRIVER = "ODBC Driver 17 for SQL Server"

SQL_PATH = PROJECT_ROOT   / "sql"  / "01_create_database.sql"