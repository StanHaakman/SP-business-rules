import operator
import os
import pandas as pd
from collections import Counter
from sys import platform

from _functions._base_functions import create_table, empty_db_table, get_id_from_dict_in_list, connect_to_db, \
    update_many_query
from classes.pymongo_converter import Converter
from classes.sessions_filter import FilterSessions

CSV_location = 'database_interactions/CSV/' if platform == "darwin" else "database_interactions\\CSV\\"
absolutepath = os.getcwd()


def create_popular_products():
    def get_popular_products(df):
        new_list = list(df['products'])
        test = list(Counter(map(get_id_from_dict_in_list, new_list)))
        popular_ids = pd.DataFrame(data={'ids': test})

        return popular_ids

    def update_popular_products(con):

        values = pd.read_sql_query('select idproducts, category, sub_category, sub_sub_category, target, doelgroep from products', con)

        for i, row in values.iterrows():
            query_fill = f"""UPDATE popular_products set category = '%s', sub_category = '%s', sub_sub_category = '%s', target = '%s', doelgroep = '%s' where idproducts = '%s';""" % (
                row['category'], row['sub_category'], row['sub_sub_category'], row['target'], row['doelgroep'], row['idproducts'])
            cur.execute(query_fill)

        con.commit()


    empty_db_table(tablename='popular_products')

    converter = Converter()

    # converter.sessions(fieldnames=['has_sale', '_id', 'order.products'], filename=f'sessions_has_sale.csv')

    filter_sessions = FilterSessions()

    filter_sessions.load_dataframe(filename=f'{CSV_location}sessions_has_sale.csv')
    # filter_sessions.has_filter()
    # filter_sessions.drop_column(['has_sale', '_id'])
    df = filter_sessions.fix_alles()
    filter_sessions.save_dataframe(filename=f'{CSV_location}sessions_has_sale.csv')

    popular_id_list = get_popular_products(df)

    tablename = 'popular_products'
    columns = '_id SERIAL NOT NULL, idproducts VARCHAR NOT NULL, category VARCHAR NULL, sub_category VARCHAR NULL, sub_sub_category VARCHAR NULL, target VARCHAR NULL, doelgroep VARCHAR NULL'

    create_table(tablename, columns)

    con = connect_to_db()
    cur = con.cursor()

    for i, row in popular_id_list.iterrows():
        query_fill = f"""INSERT INTO popular_products (idproducts) VALUES('%s');""" % (
            row['ids'])
        cur.execute(query_fill)

    update_popular_products(con)

    con.commit()
    con.close()

