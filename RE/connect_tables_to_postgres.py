import os
from sys import platform

from _functions._base_functions import empty_db_table, update_many_query
from classes.profiles_filter import FilterProfiles
from classes.pymongo_converter import Converter
from classes.send_data import DataSender
from classes.sessions_filter import FilterSessions

CSV_location = 'RE/CSV/' if platform == "darwin" else "RE\\CSV\\"
absolutepath = os.getcwd()

converter = Converter()

converter.sessions(fieldnames=['buid', '_id', 'user_agent.identifier'], filename='sessions_buids.csv')

converter.profiles(fieldnames=['_id', 'buids'], filename='profiles_buids.csv')


# Filter the sessions_buids.csv
filter_buids_sessions = FilterSessions()
filter_buids_sessions.load_dataframe(filename=f'{CSV_location}sessions_buids.csv')
filter_buids_sessions.drop_column(['identifier'])
filter_buids_sessions.replace_buids()
filter_buids_sessions.drop_null('buid')
filter_buids_sessions.drop_duplicates('buid')
filter_buids_sessions.save_dataframe(filename=f'{CSV_location}sessions_buids.csv')

filter_buids_profiles = FilterProfiles()
filter_buids_profiles.load_dataframe(filename=f'{CSV_location}profiles_buids.csv')
filter_buids_profiles.drop_null(columm_names=['_id', 'buids'])
filter_buids_profiles.drop_empty_buids()
visitor_buids = filter_buids_profiles.filter_buids()
filter_buids_profiles.save_dataframe(filename=f'{CSV_location}profiles_buids.csv')

data_sender = DataSender()

data_sender.copy_sessions_buids_csv(pathname=absolutepath + '{}{}sessions_buids.csv'.format('/' if platform == "darwin"
                                                                                         else '\\', CSV_location))
tablename = 'buids'

data_sender.copy_sessions_buids_csv(pathname=absolutepath + '{}{}sessions_buids.csv'.format('/' if platform == "darwin"
                                                                                            else '\\', CSV_location))
for i, idprofile in enumerate(visitor_buids['_id']):
    idvisitor = i + 1
    buids = list(eval(visitor_buids['buids'][i]))
    values = []
    for buid in buids:
        values.append((idvisitor, buid))
    update_many_query(tablename=tablename, change_column_name='visitors_idvisitors', change_condition_name='buids', values=values)

    if i % 10000 == 0:
        print('{} record stored...'.format(i))
