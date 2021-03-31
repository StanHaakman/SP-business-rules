import datetime
from ast import literal_eval
from dateutil import parser
import pandas as pd
import numpy as np

# Pandas dataframe volledig weergeven.
# pd.set_option('display.max_rows', None, 'display.max_columns', None,
#               'display.width', None, 'display.max_colwidth', None)
# # Pandas DataFrame wetenschappelijke notatie onderdrukken.
# pd.set_option('display.float_format', lambda x: '%.3f' % x)
#
# df = pd.read_csv('profiles.csv', encoding='utf-8')
# print(df.columns)
# print('profiles-dataset is ingeladen en wordt nu bewerkt.')
#
# for kolom in ['first', 'latest']:
#     lst = []
#     for value in df[kolom]:
#         value = parser.parse(value)
#         lst.append(value.strftime('%Y-%m-%d'))
#     df[kolom] = lst
#
# false = ['JUDGER', 'BOUNCER', 'COMPARER', 'BUYER', 'BROWSER', 'LEAVER', 'bouncer',
#          'leaver', 'comparator', 'judger', 'FUN_SHOPPER', 'browser', 'buyer', 'SHOPPING_CART']
# for value in false:
#     df['segment'] = df['segment'].replace(value, value[0].upper() + value[1:].lower(), regex=True)
#
# df['ids'] = df['ids'].apply(literal_eval)
# ids = list(df['ids'])
# lst = []
# for i in ids:
#     lst1 = []
#     for j in i:
#         if j[:3] != 'dd:':
#             lst1.append(j)
#     lst.append(lst1)
# df['ids'] = lst
#
# df.columns = ['visitor_id', 'buids', 'laatste_bezoek', 'products_aantal_verkocht', 'eerste_bezoek',
#               'products_gekocht', 'klant_type', 'products_bekeken', 'products_vergelijkbaar',
#               'aantal_paginas_bekeken', 'products_eerder_aanbevolen']  # bepaal kolomnamen.
#
# df = df[['visitor_id', 'products_gekocht', 'products_aantal_verkocht', 'products_bekeken',
#          'klant_type', 'eerste_bezoek', 'laatste_bezoek', 'products_vergelijkbaar',
#          'products_eerder_aanbevolen', 'aantal_paginas_bekeken', 'buids']]  # bepaal kolomvolgorde.
#
# df.to_csv('profiles.csv', index=False)  # opslaan naar csv
# print('profiles-dataset is verbeterd en opgeslagen.')


class FilterProfiles:
    def __init__(self):
        print('Filter processen gestart!')
        # Pandas dataframe display completely
        pd.set_option('display.max_rows', None, 'display.max_columns', None,
                  'display.width', None, 'display.max_colwidth', None)

        # Pandas DataFrame scientific display
        pd.set_option('display.float_format', lambda x: '%.3f' % x)

    def load_dataframe(self, filename):
        # Pandas bestand inzelen
        self.dataframe = pd.read_csv(filename, encoding='utf-8')

    def drop_null(self, column_names):
        self.dataframe.dropna(subset=column_names, inplace=True)

    def drop_columns(self, column_names):
        self.dataframe.drop(column_names, axis='columns', inplace=True)

    def save_dataframe(self, filename='profiles.csv'):
        self.dataframe.to_csv(filename, index=False)  # opslaan naar csv
        print('CSV bestand opgeslagen')

    def drop_empty_buids(self):
        self.dataframe.drop(self.dataframe[self.dataframe.buids == '[]'].index, inplace=True)

    def filter_buids(self):
        return self.dataframe.to_dict(orient='list')

    def replace_null(self, columns, replacement='onbekend'):
        for column in columns:
            self.dataframe[column] = self.dataframe[column].replace(np.nan, replacement, regex=True)

    def fix_alles(self):
        self.dataframe.to_json(orient='records')

        lst = []
        for i in self.dataframe['order']:
            lst.append(i)

        profiles_list = []
        for i in lst:
            if type(i) != float:
                res = dict(eval(i))
                to_remove = ['first', 'latest', 'count']

                for key_to_remove in to_remove:
                    try:
                        del res[key_to_remove]
                    except KeyError:
                        pass

                try:
                    new_list = []

                    for j, id in enumerate(res['ids']):
                        if id[:3] != 'dd:':
                            new_list.append(id)
                    res['ids'] = new_list

                    if len(res['ids']) == 0:
                        profiles_list.append(np.nan)
                        continue
                except KeyError:
                    profiles_list.append(np.nan)
                    continue

                profiles_list.append(res['ids'])
            else:
                profiles_list.append(i)

        self.dataframe['order'] = profiles_list

