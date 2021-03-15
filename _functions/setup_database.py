import psycopg2

from configparser import ConfigParser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from _functions.config import config


def drop_database():

    # Configure parser for database.ini
    parser = ConfigParser()
    parser.read('database.ini')

    # If Database line exists remove it otherwise pass
    try:
        parser.remove_option('postgresql', 'database')
        with open('database.ini', 'w') as configFile:
            parser.write(configFile)
    except ValueError:
        pass

    # Use config functie to get values from database.ini
    db = config()
    con = psycopg2.connect(**db)
    cursor = con.cursor()
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    drop_table_command = "DROP DATABASE huwebshop;"
    cursor.execute(drop_table_command)
    con.commit()
    print('Database has been dropped')
    con.close()


def create_database(dbname='huwebshop'):
    '''
    Function to create a new database and extend the database.ini file.
    :param dbname:
    :return:
    '''

    # Configure parser for database.ini
    parser = ConfigParser()
    parser.read('database.ini')

    # If Database line exists remove it otherwise pass
    try:
        parser.remove_option('postgresql', 'database')
        with open('database.ini', 'w') as configFile:
            parser.write(configFile)
    except ValueError:
        pass

    try:
        # Use config functie to get values from database.ini
        db = config()
        con = psycopg2.connect(**db)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        sqlCreateDatabase = "create database " + dbname + ";"
        cursor.execute(sqlCreateDatabase)
        con.commit()
        con.close()
        print('Database created')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    # Add database name to the database.ini file
    parser['postgresql']['database'] = dbname
    with open('database.ini', 'w') as configFile:
        parser.write(configFile)

    print(f'{dbname} aangevuld aan de database.ini file')


def fill_database(sqlfile='huwebshop.sql'):
    '''
    Fill the database with the database structure from a sql file.
    :param sqlfile:
    :return:
    '''
    db = config()
    con = psycopg2.connect(**db)
    cursor = con.cursor()
    # Open the given sql file
    with open(sqlfile, 'r') as file:
        content_list = [line.rstrip(';') for line in file]

        tempLst = []
        for i in content_list:
            if i[:2] != '--' and i != '\n':
                tempLst.append(i[:-1])
        content_list = tempLst

        separator = ' '
        content = separator.join(content_list)
        content_list = content.split(';')

        tempLst = []
        for i in content_list:
            tempLst.append(i + ';')
        tempLst.remove(tempLst[-1])
        content_list = tempLst

        for i in content_list:
            cursor.execute(i)
            con.commit()
        con.close()
