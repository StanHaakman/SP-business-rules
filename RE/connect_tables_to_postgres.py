import os
from sys import platform

from RE.classes.pymongo_converter import Converter
from RE.classes.send_data import DataSender
from RE.classes.sessions_filter import FilterSessions

CSV_location = 'CSV/' if platform == "darwin" else "CSV\\"
absolutepath = os.getcwd()

converter = Converter()

# converter.sessions(fieldnames=['buid', '_id', 'user_agent.identifier'], filename='sessions_buids.csv')

converter.profiles(fieldnames=['_id', 'buids'], filename='profiles_buids.csv')

filter_buids = FilterSessions()
filter_buids.load_dataframe(filename=f'{CSV_location}sessions_buids.csv')
filter_buids.drop_column(['identifier'])
filter_buids.replace_buids()
filter_buids.drop_null('buid')
filter_buids.drop_duplicates('buid')
filter_buids.save_dataframe(filename=f'{CSV_location}sessions_buids.csv')

data_sender = DataSender()

data_sender.copy_sessions_buids_csv(pathname=absolutepath + '{}{}sessions_buids.csv'.format('/' if platform == "darwin"
                                                                                            else '\\',CSV_location))
