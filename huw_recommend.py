import itertools

import psycopg2
from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv

from RE._functions.config import config

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
        query = "select idproducts from popular_products"
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
    def get_ad_products(self):
        db = config()
        con = psycopg2.connect(**db)
        cur = con.cursor()
        query = "select idproducts from acties order by RANDOM() limit 4"
        cur.execute(query)
        con.commit()
        row = list(cur.fetchall())
        list_items = []
        for i in row:
            list_items.append(i[0])
        con.close()
        return list_items

    def get(self, profileid, count):
        proids = self.get_ad_products()
        return proids


# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(SimpleRecom, "/<string:profileid>/<int:count>")
api.add_resource(AdRecom, "/winkelmand/<string:profileid>/<int:count>")
api.add_resource(AdRecom, '/home/<string:profileid>/<int:count>')
