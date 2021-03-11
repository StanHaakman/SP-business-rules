from classes.poducts_filter import Filter_products
from classes.pymongo_converter import Converter

'''
Create converter and select the wanted fieldnames.
Also give the name of the file u want to create.
'''

converter = Converter()
converter.products(fieldnames=['_id', 'name', 'brand', 'category', 'deeplink', 'fast_mover', 'gender', 'herhaalaankopen', 'price.selling_price', 'properties.doelgroep'], filename='products.csv')

'''

'''
filter_products = Filter_products()
filter_products.replace_null(columns=['_id', 'name', 'brand', 'category', 'deeplink', 'fast_mover', 'gender', 'herhaalaankopen', 'selling_price', 'doelgroep'])
filter_products.replace_doelgroep()
filter_products.replace_gender(invalid=['Gezin', 'B2B', 'Kinderen', 'Senior', 'Baby', 'Grootverpakking', '8719497835768'])
filter_products.save_dataframe()
