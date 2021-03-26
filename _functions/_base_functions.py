import psycopg2

from configparser import ConfigParser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from _functions.config import config


def drop_table(tablename):
    try:
        con = connect_to_db()
        cur = con.cursor()
        cur.execute(f'DROP TABLE {tablename};')
        con.commit()
        con.close()
        print(f'Table {tablename} dropped')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def connect_to_db():
    try:
        # Use config functie to get values from database.ini
        db = config()
        con = psycopg2.connect(**db)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

    return con


def create_table(tablename, columns):
    try:
        con = connect_to_db()
        cur = con.cursor()
        cur.execute(f'CREATE TABLE {tablename} ({columns});')
        con.commit()
        con.close()
        print(f'Table {tablename} created')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def empty_db_table(tablename):
    try:
        con = connect_to_db()
        cur = con.cursor()
        cur.execute(f'TRUNCATE TABLE {tablename};')
        con.commit()
        con.close()
        print(f'Table {tablename} emptied')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()


def get_data_query(query):

    try:
        con = connect_to_db()
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        con.commit()
        con.close()
        print('Data is retrieved')
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def store_data(store_query, data):

    try:
        con = connect_to_db()
        cur = con.cursor()

        for item in data:
            print(store_query, type(item))
            cur.execute(store_query % item)

        con.commit()
        con.close()

        print('Data stored in new table')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
