import pandas as pd
import psycopg2

from recom_functions._base_functions import get_data_query_fetchone
from recom_functions.config import config


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

        lst_category = []
        lst_target = []
        df = pd.DataFrame()

        SQL_query = "select category, target from products where idproducts = '{}';"
        for id in lst_id:
            var = get_data_query_fetchone(SQL_query.format(id))
            lst_category.append(var[0])
            lst_target.append(var[1])

        df['category'] = lst_category
        df['target'] = lst_target

        return df


    def get_dataframe(self, id):
        lst = self.GetQuery(visitorID=id)
        freqs = self.freq(lst)
        filtered_ids = self.filter_freq_to_list(freqs,2)

        df = self.get_product_info_from_ids(filtered_ids)
        return df
