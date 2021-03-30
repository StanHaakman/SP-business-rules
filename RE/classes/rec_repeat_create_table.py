from _functions.config import config
import psycopg2
import pandas as pd


class CreateRepeat:

    def __init__(self):
        db = config()
        self.con = psycopg2.connect(**db)

    def get_data(self):
        con = self.con
        df = pd.read_sql_query(f"select idproducts, herhaalaankopen from products where herhaalaankopen = true;", con)
        return df

    def create_table(self):
        df = self.get_data()
        con = self.con
        cur = con.cursor()

        query_drop = f"DROP TABLE IF EXISTS repeatables CASCADE;"
        cur.execute(query_drop)

        query_create = f"CREATE TABLE repeatables (idproducts VARCHAR null, herhaalaankopen BOOLEAN);"
        cur.execute(query_create)

        for i, row in df.iterrows():
            query_fill = f"""INSERT INTO repeatables (idproducts, herhaalaankopen) VALUES('%s','%s');""" % (row['idproducts'], row['herhaalaankopen'])
            cur.execute(query_fill)

        con.commit()
        con.close()
        print(f"database repeatables created")
