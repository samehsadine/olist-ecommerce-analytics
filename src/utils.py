import pyodbc
from src.config import SQL_SERVER, SQL_DATABASE, SQL_DRIVER


def get_sql_connection(database=SQL_DATABASE, autocommit=False):

    # Établir la connexion à SQL Server
    connection = pyodbc.connect(
        f"DRIVER={{{SQL_DRIVER}}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;",
        autocommit=autocommit
    )

    return connection