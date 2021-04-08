from recom_functions.config import config
import psycopg2
import pandas as pd


class CreateRecAd:

    def __init__(self):
        db = config()
        self.con = psycopg2.connect(**db)

    def get_data(self):
        con = self.con
        df = pd.read_sql_query(
            f"select idproducts, category, sub_category, sub_sub_category, target from products where folder_actief = 'Enabled';",
            con)
        return df

    def create_table(self):
        df = self.get_data()
        con = self.con
        cur = con.cursor()

        query_drop = f"DROP TABLE IF EXISTS acties CASCADE;"
        cur.execute(query_drop)

        query_create = f"CREATE TABLE acties (idProducts VARCHAR, category VARCHAR, sub_category VARCHAR, sub_sub_category VARCHAR, target VARCHAR);"
        cur.execute(query_create)

        for i, row in df.iterrows():
            query_fill = f"INSERT INTO acties (idProducts, category, sub_category, sub_sub_category, target) VALUES('%s','%s','%s','%s','%s');" % (
            row['idproducts'], row['category'], row['sub_category'], row['sub_sub_category'], row['target'])
            cur.execute(query_fill)

        con.commit()
        con.close()
        print(f"database acties created")
