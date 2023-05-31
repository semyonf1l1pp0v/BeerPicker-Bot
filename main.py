import psycopg2
from config import host, user, password, db_name

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    a = '%Ирландия%'
    with connection.cursor() as cursor:
        cursor.execute(
            "select * from beer;"
        )
        print(cursor.fetchall())

except Exception as ex:
    print("[INFO] Error while working with PostgreSQL", ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")
