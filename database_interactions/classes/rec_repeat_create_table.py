from _functions._base_functions import get_first_from_tuple
from _functions.config import config
import psycopg2
import pandas as pd
from collections import Counter


class CreateRepeat:

    def __init__(self):
        db = config()
        self.con = psycopg2.connect(**db)

    def get_data(self):
        df = pd.read_sql_query(f"select idproducts, herhaalaankopen from products where herhaalaankopen = true;",
                               self.con)
        return df

    def get_popular_repeatables(self):
        valid_product_ids = pd.read_sql_query(
            f"select idproducts, herhaalaankopen from products where herhaalaankopen = true;",
            self.con)
        session_product_ids = pd.read_sql_query(f"select products from sessions where has_sale = true", self.con)

        valid_idproducts_list = valid_product_ids['idproducts'].to_list()
        new_list = []
        for i in session_product_ids['products']:
            temp_lst = list(eval(i))
            for y in temp_lst:
                if y in valid_idproducts_list:
                    new_list.append(y)
                else:
                    pass

        repeatables = pd.DataFrame(data={'ids': list(map(get_first_from_tuple, Counter(new_list).most_common(500)))})

        return repeatables

    def create_table_repeat(self):
        df = self.get_data()
        con = self.con
        cur = con.cursor()

        query_drop = f"DROP TABLE IF EXISTS repeatables CASCADE;"
        cur.execute(query_drop)

        query_create = f"CREATE TABLE repeatables (idproducts VARCHAR null, herhaalaankopen BOOLEAN);"
        cur.execute(query_create)

        for i, row in df.iterrows():
            query_fill = f"""INSERT INTO repeatables (idproducts, herhaalaankopen) VALUES('%s','%s');""" % (
                row['idproducts'], row['herhaalaankopen'])
            cur.execute(query_fill)

        con.commit()
        print(f"database repeatables created")

    def create_table_repeat_popular(self):
        cur = self.con.cursor()

        query_drop = f"DROP TABLE IF EXISTS popular_repeatables CASCADE;"
        cur.execute(query_drop)

        query_create = f"CREATE TABLE popular_repeatables (idproducts VARCHAR null);"
        cur.execute(query_create)

        repeatables = self.get_popular_repeatables()
        for i, row in repeatables.iterrows():
            query_fill = f"""INSERT INTO popular_repeatables (idproducts) VALUES('%s');""" % (
                row['ids'])
            cur.execute(query_fill)
        self.con.commit()

    def close_con(self):
        self.con.close()
