from _functions._base_functions import where_clause
import itertools
import psycopg2


def getItemIDs(profileID):
    con = psycopg2.connect(
        host='localhost',
        password='postgres',
        user='postgres',
        database='huwebshop'
    )
    cur = con.cursor()

    buidsquery = f"SELECT buids FROM visitors WHERE (idvisitors = '{profileID}')"
    cur.execute(buidsquery)
    buidslist = cur.fetchall()

    finalbuids = (list(itertools.chain(*buidslist)))
    try:
        finalbuids = eval(finalbuids[0])
    except:
        pass

    whereclause_buids = where_clause("buid", finalbuids)
    query = f"SELECT products FROM sessions {whereclause_buids}"
    cur.execute(query)
    productlist = cur.fetchall()
    prodidlist = list(itertools.chain(*productlist))
    try:
        prodidlist = eval(prodidlist[0])
    except:
        pass

    whereclauseids = where_clause("idproducts", prodidlist)
    newquery = f"SELECT idproducts FROM repeatables {whereclauseids}"

    cur.execute(newquery)
    idlist = cur.fetchall()
    finalidlist = list(itertools.chain(*idlist))


    con.commit()
    cur.close()
    con.close()

    return finalidlist

print(getItemIDs('5a393ef6a825610001bb6c51'))
print(getItemIDs('5a394aa8a825610001bb7aed'))