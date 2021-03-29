import os
from sys import platform

import numpy as np

from RE._functions._base_functions import empty_db_table, update_many_query
from RE.classes.profiles_filter import FilterProfiles
from RE.classes.pymongo_converter import Converter
from RE.classes.send_data import DataSender
from RE.classes.sessions_filter import FilterSessions

CSV_location = 'CSV/' if platform == "darwin" else "CSV\\"
absolutepath = os.getcwd()

converter = Converter()

# converter.sessions(fieldnames=['buid', '_id', 'user_agent.identifier'], filename='sessions_buids.csv')

# converter.profiles(fieldnames=['_id', 'buids', 'recommendations.segment', 'recommendations.latest_visit'], filename='profiles_buids.csv')


# # Filter the sessions_buids.csv
filter_buids_sessions = FilterSessions()
filter_buids_sessions.load_dataframe(filename=f'{CSV_location}sessions_buids.csv')
# filter_buids_sessions.drop_column(['identifier'])
# filter_buids_sessions.replace_buids()
# filter_buids_sessions.drop_null('buid')
# filter_buids_sessions.drop_duplicates('buid')
buids_df = filter_buids_sessions.get_dataframe()
filter_buids_sessions.save_dataframe(filename=f'{CSV_location}sessions_buids.csv')

filter_buids_profiles = FilterProfiles()
filter_buids_profiles.load_dataframe(filename=f'{CSV_location}profiles_buids.csv')
filter_buids_profiles.drop_null(column_names=['_id', 'buids'])
# filter_buids_profiles.drop_null(column_names=['_id', 'buids', 'segment', 'latest_visit'])
# filter_buids_profiles.drop_columns(column_names=['segment', 'latest_visit'])
filter_buids_profiles.drop_empty_buids()
visitor_buids = filter_buids_profiles.filter_buids()
filter_buids_profiles.save_dataframe(filename=f'{CSV_location}profiles_buids.csv')

data_sender = DataSender()

data_sender.copy_sessions_buids_csv(pathname=absolutepath + '{}{}sessions_buids.csv'.format('/' if platform == "darwin"
                                                                                         else '\\', CSV_location))
tablename = 'buids'

buids = buids_df['visitors_idvisitors'] = np.nan

    if i % 10000 == 0:
        print('{} record stored...'.format(i))