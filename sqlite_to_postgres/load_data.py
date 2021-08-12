import os
import csv
import sqlite3
import psycopg2
from dotenv import load_dotenv
from sqlite3 import Cursor as _sqlite_cursor
from psycopg2.extensions import cursor as _pg_cursor
from os import remove

load_dotenv()


def save_csv(file_name: str, cur: _sqlite_cursor):
    """Сохранение csv файла."""

    with open(f"{file_name}.csv", "w") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerows(cur)


def copy_csv_to_postgresql(table_name: str, pg_cur: _pg_cursor):
    """Перенос данных из csv файла в базу postgresql."""

    with open(f"{table_name}.csv", "r") as f:
        pg_cur.copy_from(f, table_name, null="", sep="|")


def transfer_data_from_sqlite() -> None:
    """Перенос данных из sqlite."""

    pg_conn = psycopg2.connect(
        dbname=os.environ.get("DATABASE_NAME"),
        user=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD"),
        host=os.environ.get("DATABASE_HOST"),
        port=os.environ.get("DATABASE_PORT"),
        options=os.environ.get("DATABASE_OPTIONS"),
    )
    sqlite_conn = sqlite3.connect("db.sqlite")
    table_names = (
        "person",
        "genre",
        "film_work",
        "person_film_work",
        "genre_film_work",
    )

    sqlite_cur = sqlite_conn.cursor()
    pg_cur = pg_conn.cursor()

    for table_name in table_names:
        sqlite_cur.execute(f"select * from {table_name}")
        save_csv(table_name, sqlite_cur)
        copy_csv_to_postgresql(table_name, pg_cur)
        remove(f"{table_name}.csv")

    pg_conn.commit()
    pg_cur.close()
    pg_conn.close()
    sqlite_cur.close()
    sqlite_conn.close()


if __name__ == "__main__":
    transfer_data_from_sqlite()
