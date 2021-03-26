import operator
import psycopg2
import itertools
from _functions.config import config
import pandas as pd

def getPopularID(filename):


    idDict = {}

    df = pd.read_csv(filename)

    products_list = []
    for i in df['products']:
        products_list.append(i)


    print(products_list)



    # for i in df['products']:
    #     i = list(i)
    #     for j in i:
    #         if j not in idDict.keys():
    #             idDict[j] = 1
    #         else:
    #             idDict[j] += 1
    #
    # sorted_idDict = dict(sorted(idDict.items(), key=operator.itemgetter(1), reverse=True))
    #
    # return sorted_idDict






    #
    #
    # return True
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # # create query
    # query = "SELECT products_idproducts FROM orders a " \
    #         "FULL JOIN sessions c ON a.sessions_idsessions = c.idsessions " \
    #         "FULL JOIN has_sale g ON c.idsessions = g.sessions_idsessions " \
    #         "WHERE (g.has_sale = true)"
    #
    # # execute query and save results
    # cur.execute(query)
    # con.commit()
    # items = cur.fetchall()
    # print(items)
    #
    # # turn result list of tuples to regular list
    # newitems = list(itertools.chain(*items))
    # print(newitems)
    #
    # # create dict keeping track of how many times item has been bought
    # for i in newitems:
    #     if i not in idDict.keys():
    #         idDict[i] = 1
    #     else:
    #         idDict[i] += 1
    #
    # # sorteer de dictionary op hoogste values
    # sorted_idDict = dict(sorted(idDict.items(), key=operator.itemgetter(1), reverse=True))
    #
    # return sorted_idDict

