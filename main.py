from classes.pymongo_uitlezen import Converter

converter = Converter()

converter.products(fieldnames=['_id', 'brand', 'category', 'color', 'gender', 'herhaalaankopen',
                  'name', 'price.selling_price', 'properties.doelgroep', 'properties.soort',
                  'properties.variant', 'sub_category', 'sub_sub_category'], filename='products.csv')
