import psycopg2
from psycopg2 import sql

dbname = "hoteldb"
user = "postgres"
password = "1111"
host = 'localhost'
port = '5432'


# Функция для создания базы данных
def create_database():
    conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
    except psycopg2.errors.DuplicateDatabase:
        print("База данных уже существует")
    except Exception as e:
        print("Ошибка при создании базы данных:", e)
    finally:
        cursor.close()
        conn.close()


def create_tables():
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    # Создание таблицы guests
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guests (
        passport_id VARCHAR(11) PRIMARY KEY,
        fullname VARCHAR(200),
        year_of_birth INT,
        address VARCHAR(100),
        reason TEXT
    )
    """)

    # Создание таблицы rooms
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
        room_id VARCHAR(4) PRIMARY KEY,
        capacity INT,
        rooms_count INT,
        bathroom BOOLEAN,
        equipment TEXT
    )
    """)

    # Создание таблицы registration
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registration (
        room_key VARCHAR(4) REFERENCES rooms(room_id),
        guest VARCHAR(11) REFERENCES guests(passport_id),
        date_check_in DATE,
        date_depart DATE,
        status VARCHAR(9)
    )
    """)

    cursor.close()
    conn.close()


create_database()

create_tables()
