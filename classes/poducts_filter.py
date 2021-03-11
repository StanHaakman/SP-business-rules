import pandas as pd
import numpy as np

# Pandas dataframe display completely
# pd.set_option('display.max_rows', None, 'display.max_columns', None,
#               'display.width', None, 'display.max_colwidth', None)
#
# # Pandas DataFrame scientific display
# pd.set_option('display.float_format', lambda x: '%.3f' % x)
#
# # Pandas bestand inzelen
# df = pd.read_csv('products.csv', encoding='utf-8')
#
# print('Dataset ingeladen en wordt bewerkt.')
#
# print(df['herhaalaankopen'].value_counts())
# exit()

# kolommen = ['brand', 'category', 'color', 'gender', 'doelgroep', 'soort', 'variant',
#             'sub_category', 'sub_sub_category']

# for kolom in kolommen:
#     df[kolom] = df[kolom].replace(np.nan, 'onbekend', regex=True)

# df['color'] = df['color'].where(df['color'] != 'Gezin', 'onbekend') # Invalid
# df['color'] = df['color'].where(df['color'] != '4005808639892', 'onbekend')
#
# vals_lijst = ['Gezin', 'B2B', 'Kinderen', 'Senior', 'Baby', 'Grootverpakking', '8719497835768']
# for vals in vals_lijst:
#     df['gender'] = df['gender'].where(df['gender'] != vals, 'onbekend')

# df['herhaalaankopen'] = df['herhaalaankopen'].replace(np.nan, False, regex=True)

# df['doelgroep'] = df['doelgroep'].where(df['doelgroep'] != 'Geen', 'onbekend')
# df['doelgroep'] = df['doelgroep'].where(df['doelgroep'] != 'Kantoor', 'kantoor')
# df['doelgroep'] = df['doelgroep'].where(df['doelgroep'] != 'volwassene', 'Volwassenen')

# df.columns = ['product_id', 'merk', 'categorie', 'kleur', 'geslacht', 'herhaalaankopen',
#               'naam', 'prijs', 'doelgroep', 'soort', 'variant',
#               'sub_categorie', 'sub_sub_categorie']  # bepaal kolomnamen.
#
# df = df[['product_id', 'merk', 'prijs', 'doelgroep', 'categorie',
#          'sub_categorie', 'sub_sub_categorie', 'soort', 'variant',
#          'geslacht', 'kleur', 'naam', 'herhaalaankopen']]  # bepaal kolomvolgorde.

# print(df.sample(15))

# df.to_csv('products.csv', index=False)  # opslaan naar csv
print('processen beeindigd en opgeslagen!')


class Filter_products:
    def __init__(self):
        # Pandas dataframe display completely
        pd.set_option('display.max_rows', None, 'display.max_columns', None,
                  'display.width', None, 'display.max_colwidth', None)

        # Pandas DataFrame scientific display
        pd.set_option('display.float_format', lambda x: '%.3f' % x)

        # Pandas bestand inzelen
        self.dataframe = pd.read_csv('products.csv', encoding='utf-8')

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
