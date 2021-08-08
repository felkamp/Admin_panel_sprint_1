import csv
import sqlite3
import psycopg2
from db_settings import dsl
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from os import remove


def save_csv(file_name: str, data: list):
    """Сохранение csv файла."""

    with open(f"{file_name}.csv", "w") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerows(data)


def copy_csv_to_postgresql(table_name: str, pg_conn: _connection):
    """Перенос данных из csv файла в базу postgresql."""

    with open(f"{table_name}.csv", "r") as f:
        pg_cur = pg_conn.cursor()
        pg_cur.copy_from(f, table_name, null="", sep="|")


if __name__ == "__main__":
    with sqlite3.connect("db.sqlite") as sqlite_conn, psycopg2.connect(
            **dsl, cursor_factory=DictCursor
    ) as pg_conn:
        table_names = (
            "person",
            "genre",
            "film_work",
            "person_film_work",
            "genre_film_work",
        )
        sqlite_cur = sqlite_conn.cursor()
        for table_name in table_names:
            sqlite_cur.execute(f"select * from {table_name}")
            save_csv(table_name, sqlite_cur.fetchall())
            copy_csv_to_postgresql(table_name, pg_conn)
            remove(f"{table_name}.csv")
