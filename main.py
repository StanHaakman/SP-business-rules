import time

from _functions.setup_database import create_database, fill_database
from classes.poducts_filter import FilterProducts
from classes.pymongo_converter import Converter
from classes.send_data import DataSender
from classes.sessions_filter import FilterSessions

'''
Create converter and select the wanted fieldnames.
Also give the name of the file u want to create.
'''

# Create and fill the database with the table structure
create_database()
fill_database()

converter = Converter()
converter.products(fieldnames=['_id', 'name', 'brand', 'category', 'deeplink', 'properties.doelgroep', 'fast_mover', 'gender', 'herhaalaankopen', 'price.selling_price'], filename='products.csv')

'''
Create filter and load in the file. then replace the wanted values.

After that save the new data and print te amount of <null> values in the csv file to check if the filtering process worked.
'''

filter_products = FilterProducts()
filter_products.load_dataframe(filename='products.csv')
filter_products.replace_null(columns=['_id', 'name', 'brand', 'category', 'deeplink', 'fast_mover', 'gender', 'herhaalaankopen', 'selling_price', 'doelgroep'])
filter_products.replace_doelgroep()
filter_products.replace_gender(invalid=['Gezin', 'B2B', 'Kinderen', 'Senior', 'Baby', 'Grootverpakking', '8719497835768'])
filter_products.save_dataframe()
print(filter_products.dataframe.isna().sum())

# Create sender and query the products
data_sender = DataSender()
data_sender.copy_products_csv(pathname='')

converter.visitors(fieldnames=['recommendations.latest_visit'], filename='visitors.csv')

data_sender.copy_visitors_csv(pathname='')

converter.sessions(fieldnames=['user_agent.identifier', 'session_start', 'session_end'], filename='sessions.csv')

filter_sessions = FilterSessions()
filter_sessions.load_dataframe(filename='sessions.csv')
filter_sessions.save_dataframe()

data_sender.copy_sessions_csv(pathname='')
