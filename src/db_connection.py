import pyodbc

def test_connection():
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=master;"
        "Trusted_Connection=yes;"
    )

    print("Connexion SQL Server réussie !")

    connection.close()


if __name__ == "__main__":
    test_connection()