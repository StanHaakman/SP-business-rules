from ast import literal_eval
from dateutil import parser
import pandas as pd

# Pandas dataframe volledig weergeven.
pd.set_option('display.max_rows', None, 'display.max_columns', None,
              'display.width', None, 'display.max_colwidth', None)
# Pandas DataFrame wetenschappelijke notatie onderdrukken.
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df = pd.read_csv('visitors.csv', encoding='utf-8')
print(df.columns)
print('Visitors-dataset is ingeladen en wordt nu bewerkt.')

for kolom in ['first', 'latest']:
    lst = []
    for value in df[kolom]:
        value = parser.parse(value)
        lst.append(value.strftime('%Y-%m-%d'))
    df[kolom] = lst

false = ['JUDGER', 'BOUNCER', 'COMPARER', 'BUYER', 'BROWSER', 'LEAVER', 'bouncer',
         'leaver', 'comparator', 'judger', 'FUN_SHOPPER', 'browser', 'buyer', 'SHOPPING_CART']
for value in false:
    df['segment'] = df['segment'].replace(value, value[0].upper() + value[1:].lower(), regex=True)

df['ids'] = df['ids'].apply(literal_eval)
ids = list(df['ids'])
lst = []
for i in ids:
    lst1 = []
    for j in i:
        if j[:3] != 'dd:':
            lst1.append(j)
    lst.append(lst1)
df['ids'] = lst

df.columns = ['visitor_id', 'buids', 'laatste_bezoek', 'products_aantal_verkocht', 'eerste_bezoek',
              'products_gekocht', 'klant_type', 'products_bekeken', 'products_vergelijkbaar',
              'aantal_paginas_bekeken', 'products_eerder_aanbevolen']  # bepaal kolomnamen.

df = df[['visitor_id', 'products_gekocht', 'products_aantal_verkocht', 'products_bekeken',
         'klant_type', 'eerste_bezoek', 'laatste_bezoek', 'products_vergelijkbaar',
         'products_eerder_aanbevolen', 'aantal_paginas_bekeken', 'buids']]  # bepaal kolomvolgorde.

df.to_csv('visitors.csv', index=False)  # opslaan naar csv
print('Visitors-dataset is verbeterd en opgeslagen.')


class FilterVisitors:
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

    def save_dataframe(self, filename='visitors.csv'):
        self.dataframe.to_csv(filename, index=False)  # opslaan naar csv
        print('CSV bestand opgeslagen')

    def replace_null(self, columns, replacement='onbekend'):
        for column in columns:
            self.dataframe[column] = self.dataframe[column].replace(np.nan, replacement, regex=True)

