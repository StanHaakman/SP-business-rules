import pandas as pd
import numpy as np


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

    def save_dataframe(self, filename='sessions.csv'):
        self.dataframe.to_csv(filename, index=False)  # opslaan naar csv
        print('CSV bestand opgeslagen')

    def replace_buids(self):
        buid = self.dataframe['buid'].squeeze()  # zet dataframe om naar series
        buid = buid.str.strip("[']")
        self.dataframe['buid'] = buid

    def replace_null(self, columns, replacement='onbekend'):
        for column in columns:
            self.dataframe[column] = self.dataframe[column].replace(np.nan, replacement, regex=True)
