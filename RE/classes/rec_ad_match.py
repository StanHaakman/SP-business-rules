import pandas as pd
from _functions.config import config
import psycopg2
from RE.classes.rec_prev_freq import Get_freq

class Rec_match:

    def __init__(self):
        db = config()
        self.con = psycopg2.connect(**db)
        self.get_freq = Get_freq()


    def get_visitorid(self):
        pass

    def check_match(self):
        df = self.get_freq.get_dataframe()