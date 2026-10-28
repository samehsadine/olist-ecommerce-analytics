
import re
import pandas as pd
from src.config import SILVER_PARQUET_PATH
from src.utils import get_sql_connection


def load_parquet_to_sql(parquet_path, schema, table_name):

    # 1. Lire le fichier Parquet
    df = pd.read_parquet(parquet_path)

    print(f"Table cible : {schema}.{table_name}")
    print(f"Nombre de lignes à charger : {len(df)}")

    # 2. Vérifier les noms SQL
    for name in [schema, table_name]:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise ValueError(f"Nom SQL invalide : {name}")

    # 3. Connexion à SQL Server
    connection = get_sql_connection()

    try:
        cursor = connection.cursor()

        try:
            # 4. Récupérer les colonnes de la table SQL
            cursor.execute("""
                SELECT c.name
                FROM sys.columns AS c
                INNER JOIN sys.tables AS t
                    ON c.object_id = t.object_id
                INNER JOIN sys.schemas AS s
                    ON t.schema_id = s.schema_id
                WHERE s.name = ?
                AND t.name = ?
                AND c.is_identity = 0
                AND c.is_computed = 0
                ORDER BY c.column_id
            """, schema, table_name)

            sql_columns = [row[0] for row in cursor.fetchall()]

            if not sql_columns:
                raise ValueError("La table SQL n'existe pas.")

            # 5. Vérifier les colonnes du Parquet
            if set(df.columns) != set(sql_columns):
                raise ValueError(
                    f"Colonnes différentes : "
                    f"Parquet={df.columns.tolist()}, "
                    f"SQL={sql_columns}"
                )

            # Respecter l'ordre des colonnes SQL
            df = df[sql_columns]

            # 6. Convertir les valeurs manquantes en NULL
            df = df.astype(object).where(pd.notna(df), None)

            # Convertir les dates Pandas en datetime Python
            for col in df.columns:
                df[col] = df[col].map(
                    lambda value: value.to_pydatetime()
                    if isinstance(value, pd.Timestamp)
                    else value
                )

            # 7. Construire la requête INSERT
            columns = ", ".join(
                f"[{col}]" for col in sql_columns
            )

            placeholders = ", ".join(
                ["?"] * len(sql_columns)
            )

            sql = f"""
                INSERT INTO [{schema}].[{table_name}]
                ({columns})
                VALUES ({placeholders})
            """

            # 8. Préparer les données
            rows = list(
                df.itertuples(index=False, name=None)
            )
            cursor.execute(f"DELETE FROM [{schema}].[{table_name}]")
            # 9. Insérer les données
            cursor.fast_executemany = True
            cursor.executemany(sql, rows)

            # 10. Valider le chargement
            connection.commit()

            print("Chargement terminé avec succès !")

        finally:
            cursor.close()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":

    load_parquet_to_sql(
        SILVER_PARQUET_PATH / "orders.parquet",
        "silver",
        "Orders"
    )

    load_parquet_to_sql(
            SILVER_PARQUET_PATH / "customers.parquet",
            "silver",
            "Customers"
        )
    load_parquet_to_sql(
                SILVER_PARQUET_PATH / "orders_items.parquet",
                "silver",
                "OrdersItems"
            )

    load_parquet_to_sql(
                SILVER_PARQUET_PATH / "orders_payments.parquet",
                "silver",
                "OrdersPayments"
            )
    load_parquet_to_sql(
                SILVER_PARQUET_PATH / "sellers.parquet",
                "silver",
                "Sellers"
            )
    load_parquet_to_sql(
                    SILVER_PARQUET_PATH / "geolocation.parquet",
                    "silver",
                    "Geolocation"
                )
    
