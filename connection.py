import psycopg2
from config import host, user, password, db_name


def collect_beer(beer_region, beer_type, beer_style, beer_price_low, beer_price_high):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                f"select * from beer where region like '%{beer_region}%' and \
                type like '%{beer_type}%' and style like '%{beer_style}%' and \
                (price between {beer_price_low} and {beer_price_high} \
                or price_disc between {beer_price_low} and {beer_price_high});"
            )
            data = cursor.fetchall()

    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

    return data

