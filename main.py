from classes.pymongo_uitlezen import Converter

'''
Create converter and select the wanted fieldnames.
Also give the name of the file u want to create.
'''
converter = Converter()
converter.products(fieldnames=['_id', 'name', 'brand', 'category', 'deeplink', 'fast_mover', 'gender', 'herhaalaankopen', 'price.selling_price'], filename='products.csv')
