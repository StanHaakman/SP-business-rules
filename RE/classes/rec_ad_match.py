import pandas as pd
import psycopg2
from RE.classes.rec_prev_freq import Get_freq


class Rec_match:

    def __init__(self, con):
        self.con = con
        self.get_freq = Get_freq()
        self.cur = self.con.cursor()

    def filter_lst(self, lst):
        new_lst = []
        print(lst)
        for i in lst:
            try:
                for j in i:
                    new_lst.append(j[0])
            except ValueError:
                print(ValueError)
        return new_lst

    def check_match(self, df):
        lst = []
        cur = self.cur
        empty_lst = []
        print(df)

        for i, row in df.iterrows():
            query_get = f"select idproducts from acties where category = '{row['category']}' and target = '{row['target']}' order by random() limit 2;"
            cur.execute(query_get)
            data = cur.fetchall()
            if data == empty_lst:
                query_get = f"select idproducts from acties where category = '{row['category']}' order by random() limit 2;"
                cur.execute(query_get)
                data = cur.fetchall()
            lst.append(data)

        lst = self.filter_lst(lst=lst)
        return lst