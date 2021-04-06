import os
from sys import platform

from rec_popular_products import create_popular_products
from _functions.setup_database import create_database, fill_database, drop_database
from classes.products_filter import FilterProducts
from classes.profiles_filter import FilterProfiles
from classes.sessions_filter import FilterSessions
from classes.pymongo_converter import Converter
from classes.send_data import DataSender
from classes.rec_ad_create_tabel import Create_rec_ad
from classes.rec_repeat_create_table import CreateRepeat


CSV_location = 'RE/CSV/' if platform == "darwin" else "RE\\CSV\\"

absolutepath = os.getcwd()

# Create and fill the database with the table structure
drop_database(dbname='huwebshop')
create_database()
fill_database()

# Convert the main database content
converter = Converter()
converter.products(fieldnames=['_id', 'name', 'brand', 'category', 'sub_category', 'sub_sub_category', 'deeplink', 'properties.doelgroep', 'fast_mover', 'gender', 'herhaalaankopen', 'price.selling_price', 'properties.folder_actief', 'properties.discount'], filename='products.csv')

converter.profiles(fieldnames=['_id', 'recommendations.segment',  'previously_recommended', 'buids'], filename='profiles.csv')

converter.sessions(fieldnames=['_id', 'user_agent.identifier', 'has_sale', 'buid', 'order.products'], filename='sessions.csv')

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
filter_products.replace_ids()
filter_products.save_dataframe(filename=f'{CSV_location}products.csv')

filter_profiles = FilterProfiles()
filter_profiles.load_dataframe(filename=f'{CSV_location}profiles.csv')
filter_profiles.drop_null(column_names=['_id', 'segment'])
filter_profiles.save_dataframe(filename=f'{CSV_location}profiles.csv')

filter_sessions = FilterSessions()
filter_sessions.load_dataframe(filename=f'{CSV_location}sessions.csv')
filter_sessions.replace_buids()
filter_sessions.refactor_products()
filter_sessions.save_dataframe(filename=f'{CSV_location}sessions.csv')

# Create sender and copy the main files
data_sender = DataSender()
data_sender.copy_products_csv(pathname=absolutepath + '{}{}products.csv'.format('/' if platform == "darwin" else "\\",
                                                                                CSV_location))

data_sender.copy_profiles_csv(pathname=absolutepath + '{}{}profiles.csv'.format('/' if platform == "darwin" else '\\',
                                                                                CSV_location))

data_sender.copy_sessions_csv(pathname=absolutepath + '{}{}sessions.csv'.format('/' if platform == "darwin" else '\\',
                                                                                CSV_location))
create_popular_products()

Create_rec_ad().create_table()

create = CreateRepeat()
create.create_table_repeat()
create.create_table_repeat_popular()
create.close_con()

