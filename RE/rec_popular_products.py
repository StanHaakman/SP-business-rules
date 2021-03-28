import operator
import os
from sys import platform

from RE._functions._base_functions import create_table, store_data, empty_db_table
from RE.classes.pymongo_converter import Converter
from RE.classes.sessions_filter import FilterSessions

CSV_location = 'CSV/' if platform == "darwin" else "CSV\\"
absolutepath = os.getcwd()


def getPopularID(df):
    idDict = {}

    result = df['products'].squeeze()

    for i in result:
        try:
            if i[0]['id'] not in idDict.keys():
                idDict[i[0]['id']] = 1
            else:
                idDict[i[0]['id']] += 1
        except ValueError:
            print(ValueError)

    sorted_idDict = dict(sorted(idDict.items(), key=operator.itemgetter(1), reverse=True))

    keys_list = list(sorted_idDict.keys())
    popular_idlist = []
    for i in range(4):
        popular_idlist.append(keys_list[i])

    return popular_idlist


empty_db_table(tablename='popular_products')

converter = Converter()

converter.sessions(fieldnames=['has_sale', '_id', 'order.products'], filename='sessions_has_sale.csv')

filter_sessions = FilterSessions()

filter_sessions.load_dataframe(filename=f'{CSV_location}sessions_has_sale.csv')
filter_sessions.has_filter()
filter_sessions.drop_column(['has_sale', '_id'])
df = filter_sessions.fix_alles()
filter_sessions.save_dataframe(filename=f'{CSV_location}sessions_has_sale.csv')

popular_id_list = getPopularID(df=df)

tablename = 'Popular_products'
columns = '_id SERIAL NOT NULL, idproducts VARCHAR NOT NULL'

create_table(tablename, columns)

store_query = f"insert into {tablename} (idproducts) values (%s)"
store_data(store_query, popular_id_list)
