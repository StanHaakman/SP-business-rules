import itertools

import psycopg2
from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv

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


class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""

    def get(self, profileid, count):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. """
        randcursor = database.products.aggregate([{'$sample': {'size': count}}])
        prodids = list(map(lambda x: x['_id'], list(randcursor)))
        return prodids, 200

    def getPopularID(self):
        # DataSenderObject = DataSender()
        # con = DataSenderObject.openconnection()def connect_to_db():
        con = psycopg2.connect(
            host='localhost',
            password='postgres',
            user='postgres',
            database='huwebshop'
        )
        cur = con.cursor()

        idDict = {}

        query = "SELECT * FROM popular_products"

        cur.execute(query)
        con.commit()
        items = cur.fetchall()
        print(items)
        newitems = list(itertools.chain(*items))
        print(newitems)

        # selecteer producten in mongodb
        cursor = database.products.aggregate([{'_id': {"$in": [self.aggregateIDClause(newitems)]}}])
        prodids = list(map(lambda x: x['_id'], list(cursor)))

        return prodids, 200

    def aggregateIDClause(itemID):
        """selects the first 4 ID's in a dictionary"""
        for i in range(1):
            clause = "'{}', '{}', '{}', '{}'".format(itemID.keys(i), itemID.keys(i + 1), itemID.keys(i + 2),
                                                     itemID.keys(i + 3))


# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>")
