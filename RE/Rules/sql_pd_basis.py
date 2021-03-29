from RE._functions.config import config
import psycopg2
import pandas as pd


class ContentRules:

    def __init__(self):
        pd.set_option('display.max_rows', None, 'display.max_columns', None,
                      'display.width', None, 'display.max_colwidth', None)

    def openconnection(self):
        ''' open een connectie met postgres database'''
        db = config()
        con = psycopg2.connect(**db)
        return con


    def filter_dataframe(self, df):
        ''' filter het dataframe zodat postgresql query geen foutmeldingen meer geeft '''

        column_name = df['name']
        column_brand = df['brand']
        new_name = []
        new_brand = []

        ''' filter alles uit de column name '''
        for i in column_name:
            i = [x.replace("'", " ") for x in i]
            i = ''.join(i)
            new_name.append(i)

        ''' filter alles uit de colomn brand '''
        for i in column_brand:
            i = [x.replace("'", " ") for x in i]
            i = ''.join(i)
            new_brand.append(i)

        df['name'] = new_name
        df['brand'] = new_brand

        return df

    def filter_name(self, name):
        ''' filter functie voor namen zodat postgresql er mee kan werken '''
        name = [i.replace('-', ' ') for i in name]
        name = [i.replace('&', 'and') for i in name]
        name = [i.replace('%', 'percent') for i in name]
        name = [i.replace('0', '') for i in name]
        name = [i.replace('5', 'vijtfig') for i in name]
        name = [i.replace('=', 'is') for i in name]
        name = ''.join(name)
        name = name.replace(" ", "")

        return name

    def get_data_catagory(self, category, type):
        ''' haal de data catagory uit postgres '''

        ''' maak een connectie met de database '''
        con = self.openconnection()

        ''' maak een dataframe aan '''
        df = pd.read_sql_query(
            f"select idproducts, name, brand, category from products where {type} = '{category}' order by random() limit 10;",
            con)

        return df

    def create_table(self, target, type):
        ''' Met deze functie maak je een nieuwe tabel automatisch aan en zet je de data in de tabel'''

        ''' open een connectie met de database'''
        con = self.openconnection()
        cur = con.cursor()

        ''' haal de data op'''
        df = self.get_data_catagory(category=target, type=type)

        ''' filter de naam'''
        target = self.filter_name(name=target)

        ''' verwijder de database als die al bestaat'''
        query_drop = f"DROP TABLE IF EXISTS {target} CASCADE;"
        cur.execute(query_drop)

        ''' maak een nieuwe database aan'''
        query = f"CREATE TABLE {target} (idProducts VARCHAR(255),  name VARCHAR,  brand VARCHAR,  category VARCHAR);"
        cur.execute(query)

        ''' filter het dataframe zodat postgres de data kan lezen en versturen'''
        df = self.filter_dataframe(df=df)

        ''' zet de data in de nieuwe database '''
        for i, row in df.iterrows():
            query_fill = f"INSERT INTO {target} (idProducts, name, brand, category) VALUES('%s','%s','%s','%s');" % (row['idproducts'], row['name'], row['brand'], row['category'])
            cur.execute(query_fill)

        con.commit()
        con.close()
        print(f"database {target} created")



