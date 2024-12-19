from django.db import connection

def list_tables():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = 'consultation'
        """)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print("Table:", row[0])
        else:
            print("No tables found in schema 'consultation'.")

list_tables()
