import itertools

import psycopg2
from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv

from recom_functions.rec_discount_match import DiscountMatch
from recom_functions.rec_prev_freq import GetFreq
from recom_functions.rec_ad_match import Rec_match
from recom_functions.config import config
from recom_functions.rec_repeatables import get_herhaal_Item_IDs
from recom_functions.rec_similar_order_match import SimilarOrderMatch

app = Flask(__name__)
api = Api(app)

# We define these variables to (optionally) connect to an external MongoDB
# instance.
envvals = ["MONGODBUSER", "MONGODBPASSWORD", "MONGODBSERVER"]
dbstring = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

# Since we are asked to pass a class rather than an instance of the class to the
# add_resource method, we open the connection to the database outside of the 
# Recom class.
load_dotenv()
if os.getenv(envvals[0]) is not None:
    envvals = list(map(lambda x: str(os.getenv(x)), envvals))
    client = MongoClient(dbstring.format(*envvals))
else:
    client = MongoClient()
database = client.huwebshop


class SimpleRecom(Resource):
    def get_popular_products(self):
        # con = psycopg2.connect(
        #     host='localhost',
        #     password='Elvis&Presley',
        #     user='postgres',
        #     database='huwebshop'
        # )

        db = config()
        con = psycopg2.connect(**db)
        cur = con.cursor()
        query = "select idproducts from popular_products limit(4)"
        cur.execute(query)
        con.commit()
        row = list(cur.fetchall())
        list_items = []
        for i in row:
            list_items.append(i[0])
        con.close()
        return list_items

    def get(self, profileid, count):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. """
        prodids = self.get_popular_products()
        return prodids, 200


class AdRecom(Resource):

    def get_ad_products(self, profileid):
        df = GetFreq().get_dataframe(id=profileid)
        lst = Rec_match().check_match(df=df)
        return lst

    def get(self, profileid, count):
        proids = self.get_ad_products(profileid)
        return proids


class RepRecom(Resource):
    def get_rep_products(self, profileid):
        list_items = get_herhaal_Item_IDs(profileid)

        return list_items

    def get(self, profileid, count):
        proids = self.get_rep_products(profileid)
        return proids


class SimilarOrderRecom(Resource):
    def get_similar_products(self, productid):
        similar_product_list = SimilarOrderMatch().match(id=productid)
        return similar_product_list

    def get(self, profileid, productid, count):
        proid = self.get_similar_products(productid)
        return proid


class DiscountProductRecom(Resource):
    def get_similar_products(self, productid):
        discount_product_list = DiscountMatch().match(id=productid)
        return discount_product_list

    def get(self, profileid, productid, count):
        proid = self.get_similar_products(productid)
        return proid


# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
# Homepagina
api.add_resource(AdRecom, '/home/<string:profileid>/<int:count>')

# Productpagina
api.add_resource(RepRecom, "/<string:profileid>/<int:count>")

# Detailpagina
api.add_resource(DiscountProductRecom, '/productdetail/<string:profileid>/<string:productid>/<int:count>')

# Winkelmandje
api.add_resource(SimilarOrderRecom, "/winkelmand/<string:profileid>/<string:productid>/<int:count>")
