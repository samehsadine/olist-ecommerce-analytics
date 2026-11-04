
from src.utils import get_sql_connection
from src.config import PROJECT_ROOT


def create_silver_tables():

    # Path to the SQL script containing all Silver tables
    sql_path = PROJECT_ROOT / "sql" / "02_create_silver_tables.sql"

    # Connect to SQL Server
    connection = get_sql_connection(autocommit=True)

    try:
        # Read the SQL file
        with sql_path.open("r", encoding="utf-8") as file:
            sql_script = file.read()

        # Create the cursor
        cursor = connection.cursor()

        try:
            # Execute the SQL script
            cursor.execute(sql_script)

            print("Tables Silver créées ou déjà existantes !")

        finally:
            cursor.close()

    finally:
        connection.close()


if __name__ == "__main__":
    create_silver_tables()
