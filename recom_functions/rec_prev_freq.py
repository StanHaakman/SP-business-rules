import pandas as pd
import psycopg2

from recom_functions._base_functions import get_data_query_fetchone
from recom_functions.config import config


class GetFreq:

    def __init__(self):
        db = config()
        self.con = psycopg2.connect(**db)
        self.cur = self.con.cursor()

    def get_visitor_info(self, id):
        query = f"select previously_recommended from visitors where idvisitors = '{id}'"
        self.cur.execute(query)
        data = self.cur.fetchall()
        for i in data:
            data = eval(i[0])
        return data

    def get_df(self, lst_id):
        lst_category = []
        lst_sub_category = []
        lst_sub_sub_category = []
        lst_target = []
        df = pd.DataFrame()

        SQL_query = "select category, sub_category, sub_sub_category, target from products where idproducts = '{}';"
        for id in lst_id:
            var = get_data_query_fetchone(SQL_query.format(id))
            lst_category.append(var[0])
            lst_sub_category.append(var[1])
            lst_sub_sub_category.append(var[2])
            lst_target.append(var[3])

        df['category'] = lst_category
        df['sub_category'] = lst_sub_category
        df['sub_sub_category'] = lst_sub_sub_category
        df['target'] = lst_target

        return df

    def data_count(self, old_df):
        df = pd.DataFrame()

        try:
            df['category'] = old_df['category'].value_counts()[:2].index.tolist()
            df['sub_category'] = old_df['sub_category'].value_counts()[:2].index.tolist()
            df['sub_sub_category'] = old_df['sub_sub_category'].value_counts()[:2].index.tolist()
            df['target'] = old_df['target'].value_counts()[:2].index.tolist()
        except ValueError:
            df['category'] = old_df['category'].value_counts()[:1].index.tolist()
            df['sub_category'] = old_df['sub_category'].value_counts()[:1].index.tolist()
            df['sub_sub_category'] = old_df['sub_sub_category'].value_counts()[:1].index.tolist()
            df['target'] = old_df['target'].value_counts()[:1].index.tolist()

        return df

    def get_dataframe(self, id):
        lst = self.get_visitor_info(id=id)
        df = self.get_df(lst)
        df = self.data_count(old_df=df)
        return df
