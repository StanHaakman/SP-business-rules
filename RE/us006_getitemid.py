from _functions._base_functions import where_clause
import itertools
import psycopg2


def get_profile_buids(profileID, cur):
    buidsquery = f"SELECT buids FROM visitors WHERE (idvisitors = '{profileID}')"
    print(buidsquery)
    cur.execute(buidsquery)
    buidslist = cur.fetchall()

    finalbuids = (list(itertools.chain(*buidslist)))
    try:
        finalbuids = eval(finalbuids[0])
    except:
        pass

    return finalbuids


def get_item_ID(valuename, valuelist, cur):
    whereclause = where_clause(valuename, valuelist)
    query = f"SELECT products FROM sessions {whereclause}"
    print(query)
    cur.execute(query)
    productlist = cur.fetchall()
    prodidlist = list(itertools.chain(*productlist))
    try:
        prodidlist = eval(prodidlist[0])
    except:
        pass
    return prodidlist


def getItemIDs(profileID):

    con = psycopg2.connect(
        host='localhost',
        password='pikatoe2',
        user='postgres',
        database='huwebshop'
    )
    cur = con.cursor()

    finalbuids = get_profile_buids(profileID, cur)


    whereclauseids = where_clause("idproducts", prodidlist)
    newquery = f"SELECT idproducts FROM repeatables {whereclauseids}"
    print(newquery)

    cur.execute(newquery)
    idlist = cur.fetchall()
    finalidlist = list(itertools.chain(*idlist))


    con.commit()
    cur.close()
    con.close()

    return finalidlist

print(getItemIDs('5a393ef6a825610001bb6c51'))
print(getItemIDs('5a394aa8a825610001bb7aed'))