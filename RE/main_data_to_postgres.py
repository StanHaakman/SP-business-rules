import os
from sys import platform

from _functions.setup_database import create_database, fill_database, drop_database
from classes.products_filter import FilterProducts
from classes.profiles_filter import FilterProfiles
from classes.pymongo_converter import Converter
from classes.send_data import DataSender


CSV_location = 'RE/CSV/' if platform == "darwin" else "RE\\CSV\\"

absolutepath = os.getcwd()

# Create and fill the database with the table structure
drop_database(dbname='huwebshop')
create_database()
fill_database()

# Convert the main database content
converter = Converter()
converter.products(fieldnames=['_id', 'name', 'brand', 'category', 'deeplink', 'properties.doelgroep', 'fast_mover', 'gender', 'herhaalaankopen', 'price.selling_price', 'properties.folder_actief'], filename='products.csv')

converter.profiles(fieldnames=['_id', 'recommendations.segment',  'previously_recommended'], filename='profiles.csv')
#
converter.sessions(fieldnames=['_id', 'user_agent.identifier', 'session_start', 'session_end'], filename='sessions.csv')

'''
Create products filter and load in the file. then replace the wanted values.

After that save the new data and print te amount of <null> values in the csv file to check if the filtering process
worked.
'''

filter_products = FilterProducts()
filter_products.load_dataframe(filename=f'{CSV_location}products.csv')
filter_products.replace_null(
    columns=['_id', 'name', 'brand', 'category', 'deeplink', 'fast_mover', 'gender', 'herhaalaankopen', 'selling_price',
             'doelgroep'])
filter_products.replace_doelgroep()
filter_products.replace_gender(
    invalid=['Gezin', 'B2B', 'Kinderen', 'Senior', 'Baby', 'Grootverpakking', '8719497835768'])
filter_products.save_dataframe(filename=f'{CSV_location}products.csv')

filter_profiles = FilterProfiles()
filter_profiles.load_dataframe(filename=f'{CSV_location}profiles.csv')
filter_profiles.drop_null(column_names=['_id', 'segment', 'latest_visit'])
filter_profiles.save_dataframe()

# Create sender and copy the main files
data_sender = DataSender()
data_sender.copy_products_csv(pathname=absolutepath + '{}{}products.csv'.format('/' if platform == "darwin" else "\\",
                                                                                CSV_location))

data_sender.copy_profiles_csv(pathname=absolutepath + '{}{}profiles.csv'.format('/' if platform == "darwin" else '\\',
                                                                                CSV_location))

data_sender.copy_sessions_csv(pathname=absolutepath + '{}{}sessions.csv'.format('/' if platform == "darwin" else '\\',
                                                                                CSV_location))
