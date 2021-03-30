from _functions._base_functions import drop_table, create_table, get_data_query_fetchone, store_data
import pandas as pd
from _functions.config import config
import psycopg2




class Get_freq:

    def __init__(self):
        db = config()
        self.con = psycopg2.connect(**db)


    def GetQuery(self, visitorID):
        SQL_query = "select previously_recommended from visitors where idvisitors = '{}';".format(visitorID)
        data = get_data_query_fetchone(SQL_query)
        lst = list(eval(data[0]))
        return lst

    def freq(self, lst):
        freqs = dict()
        for x in lst:
            if x not in freqs:
                freqs.update({x:1})
                pass
            else:
                freqs[x] += 1
            pass
        return freqs


    def filter_freq_to_list(self, dict, iterator):
        lst = []

        for x in range(-1,iterator - 1):
            lst.append(list(dict)[x])
            pass
        return lst

    def get_product_info_from_ids(self, lst_id):
        SQL_query = "select category, target from products where idproducts = '{}';"
        con = self.con
        for id in lst_id:
            df = pd.read_sql_query(SQL_query.format(id),con)

        return df


    def get_dataframe(self):
        lst = self.GetQuery(visitorID="5a393d68ed295900010384ca")
        freqs = self.freq(lst)
        filtered_ids = self.filter_freq_to_list(freqs,2)

        df = self.get_product_info_from_ids(filtered_ids)

        return df
