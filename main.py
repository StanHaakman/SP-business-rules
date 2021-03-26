import os
import time

from Rules.simple_reccomendation import getPopularID
from _functions.setup_database import create_database, fill_database, drop_database
from classes.products_filter import FilterProducts
from classes.pymongo_converter import Converter
from classes.send_data import DataSender
from classes.sessions_filter import FilterSessions

'''
Create converter and select the wanted fieldnames.
Also give the name of the file u want to create.
'''

# Create and fill the database with the table structure
drop_database(dbname='huwebshop')
create_database()
fill_database()

converter = Converter()
converter.products(
    fieldnames=['_id', 'name', 'brand', 'category', 'deeplink', 'properties.doelgroep', 'fast_mover', 'gender',
                'herhaalaankopen', 'price.selling_price'], filename='products.csv')

# '''
# Create filter and load in the file. then replace the wanted values.
#
# After that save the new data and print te amount of <null> values in the csv file to check if the filtering process worked.
# '''

filter_products = FilterProducts()
filter_products.load_dataframe(filename='products.csv')
filter_products.replace_null(
    columns=['_id', 'name', 'brand', 'category', 'deeplink', 'fast_mover', 'gender', 'herhaalaankopen', 'selling_price',
             'doelgroep'])
filter_products.replace_doelgroep()
filter_products.replace_gender(
    invalid=['Gezin', 'B2B', 'Kinderen', 'Senior', 'Baby', 'Grootverpakking', '8719497835768'])
filter_products.save_dataframe(filename='products.csv')
print(filter_products.dataframe.isna().sum())

# Create sender and query the products

absolutepath = os.getcwd()

data_sender = DataSender()
data_sender.copy_products_csv(pathname=absolutepath + "/products.csv")

converter.visitors(fieldnames=['recommendations.segment', 'recommendations.latest_visit'], filename='visitors.csv')

data_sender.copy_visitors_csv(pathname=absolutepath + "/visitors.csv")

converter.sessions(fieldnames=['_id', 'user_agent.identifier', 'session_start', 'session_end'], filename='sessions.csv')

filter_sessions = FilterSessions()
filter_sessions.load_dataframe(filename='sessions.csv')
filter_sessions.save_dataframe()

data_sender.copy_sessions_csv(pathname=absolutepath + "/sessions.csv")

# propertieslst = [
#                 "bundel_sku",
#                 "doelgroep",
#                 "eenheid",
#                 "factor",
#                 "gebruik",
#                 "geschiktvoor",
#                 "geursoort",
#                 "huidconditie",
#                 "huidtype",
#                 "huidtypegezicht",
#                 "kleur",
#                 "leeftijd",
#                 "sterkte",
#                 "type",
#                 "variant",
#                 "waterproof",
#                 "folder_actief",
#                 "soort",
#                 "inhoud"
#                 ]

# for lst in propertieslst:
#    converter.products(fieldnames=['_id', 'properties.{}'.format(lst)],filename='products_properties_{}.csv'.format(lst))
#    filter_products.load_dataframe(filename='products_properties_{}.csv'.format(lst))
#    filter_products.drop_null(lst)
#    filter_products.save_dataframe(filename='products_properties_{}.csv'.format(lst))
#    data_sender.copy_products_properties_csv(pathname = absolutepath + "\products_properties_{}.csv".format(lst))
#    pass


buids_converter = Converter()

buids_converter.sessions(fieldnames=['buid', '_id', 'user_agent.identifier'], filename='sessions_buids.csv')

filter_sessions_buids = FilterSessions()
filter_sessions_buids.load_dataframe(filename='sessions_buids.csv')
filter_sessions_buids.drop_column(['identifier'])
filter_sessions_buids.replace_buids()
filter_sessions_buids.drop_null('buid')
filter_sessions_buids.drop_duplicates('buid')
filter_sessions_buids.save_dataframe(filename='sessions_buids.csv')

buids_sender = DataSender()
buids_sender.copy_sessions_buids_csv(pathname=absolutepath + "/sessions_buids.csv")

converter.sessions(fieldnames=['has_sale', '_id', 'order.products'], filename='sessions_has_sale.csv')

filter_sessions.load_dataframe(filename="sessions_has_sale.csv")
filter_sessions.has_filter()
filter_sessions.save_dataframe(filename="sessions_has_sale.csv")

print(getPopularID(filename="sessions_has_sale.csv"))
