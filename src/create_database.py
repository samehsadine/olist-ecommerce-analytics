
from src.utils import get_sql_connection

from src.config import SQL_PATH

def create_database():


    # Connexion à master pour créer la base
    connection = get_sql_connection(
        database="master",
        autocommit=True
    )

    try:
        with SQL_PATH.open("r", encoding="utf-8") as file:
            sql_script = file.read()

        cursor = connection.cursor()
        try:
            cursor.execute(sql_script)
            print("Base OlistAnalytics créée ou déjà existante !")
        finally:
            cursor.close()
    finally:
        connection.close()


if __name__ == "__main__":
    create_database()