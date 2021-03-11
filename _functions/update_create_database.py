import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def connect(db=None):
    con = psycopg2.connect(
        host='localhost',  # De host waarop je database runt
        database=db,
        user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
        password='postgres'  # Wachtwoord die je opgaf bij installatie
        # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
    )
    return con


def create_database():
    con = connect()
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()
    name = 'huwebshop'
    sqlCreateDatabase = "create database " + name + ";"
    cursor.execute(sqlCreateDatabase)
    con.commit()
    con.close()