import pandas as pd
import numpy as np


class Filter_products:
    def __init__(self):
        print('processen beeindigd en opgeslagen!')
        # Pandas dataframe display completely
        pd.set_option('display.max_rows', None, 'display.max_columns', None,
                  'display.width', None, 'display.max_colwidth', None)

        # Pandas DataFrame scientific display
        pd.set_option('display.float_format', lambda x: '%.3f' % x)

    def load_dataframe(self, filename):
        # Pandas bestand inzelen
        self.dataframe = pd.read_csv(filename, encoding='utf-8')

    def replace_null(self, columns, replacement='onbekend'):
        for column in columns:
            self.dataframe[column] = self.dataframe[column].replace(np.nan, replacement if column != 'herhaalaankopen' else False, regex=True)

    def replace_color(self, replacement='onbekend'):
        self.dataframe['color'] = self.dataframe['color'].where(self.dataframe['color'] != '4005808639892', replacement)

    def replace_doelgroep(self):
        self.dataframe['doelgroep'] = self.dataframe['doelgroep'].where(self.dataframe['doelgroep'] != 'Geen', 'onbekend')
        self.dataframe['doelgroep'] = self.dataframe['doelgroep'].where(self.dataframe['doelgroep'] != 'kantoor', 'Kantoor')
        self.dataframe['doelgroep'] = self.dataframe['doelgroep'].where(self.dataframe['doelgroep'] != 'volwassene', 'Volwassenen')
        self.dataframe['doelgroep'] = self.dataframe['doelgroep'].where(self.dataframe['doelgroep'] != 'zwangere vrouw', 'Zwangere vrouw')

    def replace_gender(self, invalid, replacement='onbekend'):
        for invalid_item in invalid:
            self.dataframe['gender'] = self.dataframe['gender'].where(self.dataframe['gender'] != invalid_item, replacement)

    def save_dataframe(self):
        self.dataframe.to_csv('products.csv', index=False)  # opslaan naar csv
        print('CSV bestand opgeslagen')
