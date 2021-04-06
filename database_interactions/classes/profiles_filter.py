import pandas as pd
import numpy as np


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

