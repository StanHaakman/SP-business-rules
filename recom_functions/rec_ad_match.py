import psycopg2

from recom_functions.config import config
from recom_functions.rec_prev_freq import GetFreq


class Rec_match:

    def __init__(self):
        db = config()
        self.con = psycopg2.connect(**db)
        self.get_freq = GetFreq()
        self.cur = self.con.cursor()

    def filter_lst(self, lst):
        new_lst = []
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
            query_get = f"select idproducts from acties where sub_sub_category = '{row['sub_sub_category']}' and target = '{row['target']}' order by random() limit 2;"
            cur.execute(query_get)
            data = cur.fetchall()
            if data == empty_lst:
                query_get = f"select idproducts from acties where sub_sub_category = '{row['sub_sub_category']}' order by random() limit 2;"
                cur.execute(query_get)
                data = cur.fetchall()
                if data == empty_lst:
                    query_get = f"select idproducts from acties where sub_category = '{row['sub_category']}' and target = '{row['target']}' order by random() limit 2;"
                    cur.execute(query_get)
                    data = cur.fetchall()
                    if data == empty_lst:
                        query_get = f"select idproducts from acties where sub_category = '{row['sub_category']}' order by random() limit 2;"
                        cur.execute(query_get)
                        data = cur.fetchall()
                        if data == empty_lst:
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