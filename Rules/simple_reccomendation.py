import operator
import psycopg2
import itertools
from _functions.config import config

import pandas as pd

def getPopularID(df):

    idDict = {}

    result = df['products'].squeeze()


    for i in result:
        if i[0]['id'] not in idDict.keys():
            idDict[i[0]['id']] = 1
        else:
            idDict[i[0]['id']] += 1

    sorted_idDict = dict(sorted(idDict.items(), key=operator.itemgetter(1), reverse=True))

    return sorted_idDict