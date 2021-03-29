import operator
import os
from sys import platform
import psycopg2

from RE._functions._base_functions import create_table, store_data, empty_db_table
from RE._functions.config import *
from RE.classes.pymongo_converter import Converter
from RE.classes.sessions_filter import FilterSessions

class Rec_popular_products:

    def __init__(self):
        db = config()
        self.con = psycopg2.connect(**db)

    def get_data(self):
        con = self.con
        cur = con.cursor()
        query = "select idproducts from popular_products"
        cur.execute(query)
        items = cur.fetchall()
        list_items = list(items)
        return list_items