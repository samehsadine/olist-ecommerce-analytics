
from src.utils import get_sql_connection
from src.config import PROJECT_ROOT


def create_silver_tables():

    # Chemin du script SQL contenant toutes les tables Silver
    sql_path = PROJECT_ROOT / "sql" / "02_create_silver_tables.sql"

    # Connexion à SQL Server
    connection = get_sql_connection(autocommit=True)

    try:
        # Lire le fichier SQL
        with sql_path.open("r", encoding="utf-8") as file:
            sql_script = file.read()

        # Créer le curseur
        cursor = connection.cursor()

        try:
            # Exécuter le script SQL
            cursor.execute(sql_script)

            print("Tables Silver créées ou déjà existantes !")

        finally:
            cursor.close()

    finally:
        connection.close()


if __name__ == "__main__":
    create_silver_tables()
