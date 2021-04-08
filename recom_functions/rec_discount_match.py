import psycopg2
import pandas as pd
from recom_functions.config import config


class DiscountMatch:

    def __init__(self):
        db = config()
        self.con = psycopg2.connect(**db)
        self.cur = self.con.cursor()

    def iddata_to_df(self, id):
        query = f"select idproducts, sub_sub_category, doelgroep, target from products where idproducts = '{id}' limit 1;"
        df = pd.read_sql_query(query, self.con)
        return df

    def match(self, id):
        df = self.iddata_to_df(id=id)

        data = []
        for i, row in df.iterrows():
            query = f"select idproducts from popular_products where sub_sub_category = '{row['sub_sub_category']}' and doelgroep = '{row['doelgroep']}' and target = '{row['target']}' and discount is not null limit 4; "
            self.cur.execute(query)
            data.append(self.cur.fetchall())

        filtered_data = [i[0] for i in data[0]]

        return filtered_data
