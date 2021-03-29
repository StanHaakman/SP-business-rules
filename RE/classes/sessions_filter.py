import pandas as pd
import numpy as np
import json


class FilterSessions:
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

    def get_dataframe(self):
        return self.dataframe

    def save_dataframe(self, filename='sessions.csv'):
        self.dataframe.to_csv(filename, index=False)  # opslaan naar csv
        print('CSV bestand opgeslagen')

    def replace_buids(self):
        buid = self.dataframe['buid'].squeeze()  # zet dataframe om naar series
        buid = buid.str.strip("[']")
        self.dataframe['buid'] = buid

    def replace_to_json(self):
        self.dataframe.to_json(orient='records')

    def replace_null(self, columns, replacement='onbekend'):
        for column in columns:
            self.dataframe[column] = self.dataframe[column].replace(np.nan, replacement, regex=True)

    def drop_null(self,columm_name):
        self.dataframe.dropna(subset=[columm_name], inplace=True)
        print(self.dataframe.isna().sum())
        pass
    
    def drop_duplicates(self,columm_names):
        self.dataframe.drop_duplicates(subset=[column_names], keep='first', inplace=True)

    def has_filter(self):

        # Get indexes where name column has value john
        indexNames = self.dataframe[self.dataframe['has_sale'] == False].index

        # Delete these row indexes from dataFrame
        self.dataframe.drop(indexNames, inplace=True)

    def fix_alles(self):

        lst = []
        for i in self.dataframe['products']:
            lst.append(i)

        products_lst = []
        for i in lst:
            temp_list = []
            temp_list.append(i)
            for j in temp_list:
                res = list(eval(j))
                products_lst.append(res)

        self.dataframe['products'] = products_lst

        return self.dataframe

    def drop_column(self, column_names):
        self.dataframe.drop(column_names, axis='columns', inplace=True)
