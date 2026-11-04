
import re
import pandas as pd
from src.config import SILVER_PARQUET_PATH
from src.utils import get_sql_connection


def load_parquet_to_sql(parquet_path, schema, table_name):

    # 1. Read the Parquet file
    df = pd.read_parquet(parquet_path)

    print(f"Table cible : {schema}.{table_name}")
    print(f"Nombre de lignes à charger : {len(df)}")

    # 2. Validate the SQL names
    for name in [schema, table_name]:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise ValueError(f"Nom SQL invalide : {name}")

    # 3. Connect to SQL Server
    connection = get_sql_connection()

    try:
        cursor = connection.cursor()

        try:
            # 4. Retrieve the SQL table columns
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

            # 5. Check the Parquet columns
            if set(df.columns) != set(sql_columns):
                raise ValueError(
                    f"Colonnes différentes : "
                    f"Parquet={df.columns.tolist()}, "
                    f"SQL={sql_columns}"
                )

            # Preserve the SQL column order
            df = df[sql_columns]
               # 6. Retrieve the SQL primary key columns
            cursor.execute("""
                SELECT c.name
                FROM sys.indexes AS i
                INNER JOIN sys.index_columns AS ic
                    ON i.object_id = ic.object_id
                    AND i.index_id = ic.index_id
                INNER JOIN sys.columns AS c
                    ON ic.object_id = c.object_id
                    AND ic.column_id = c.column_id
                INNER JOIN sys.tables AS t
                    ON i.object_id = t.object_id
                INNER JOIN sys.schemas AS s
                    ON t.schema_id = s.schema_id
                WHERE s.name = ?
                  AND t.name = ?
                  AND i.is_primary_key = 1
                ORDER BY ic.key_ordinal
            """, schema, table_name)
            primary_key_columns = [
                row[0] for row in cursor.fetchall()
            ]
            # 7. Check duplicate primary keys
            if primary_key_columns:
                duplicate_count = df.duplicated(
                    subset=primary_key_columns
                ).sum()
                if duplicate_count > 0:
                    raise ValueError(
                        f"{duplicate_count} clés primaires dupliquées "
                        f"dans {schema}.{table_name}"
                    )
                print("Vérification des clés primaires : OK")

            # 6. Convert missing values to NULL
            df = df.astype(object).where(pd.notna(df), None)

            # Convert Pandas dates to Python datetime objects
            for col in df.columns:
                df[col] = df[col].map(
                    lambda value: value.to_pydatetime()
                    if isinstance(value, pd.Timestamp)
                    else value
                )

            # 7. Build the INSERT query
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

            # 8. Prepare the data
            rows = [
                    tuple(
                        None if pd.isna(value) else value
                        for value in row
                    )
                    for row in df.itertuples(index=False, name=None)
    ]

           
            cursor.execute(f"DELETE FROM [{schema}].[{table_name}]")
            # 9. Insert the data
            cursor.fast_executemany = False
            cursor.executemany(sql, rows)

            # 10. Commit the load
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
                    SILVER_PARQUET_PATH / "order_reviews.parquet",
                    "silver",
                    "OrderReviews"
                )
    
