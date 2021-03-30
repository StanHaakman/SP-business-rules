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
    finalbuids = eval(finalbuids[0])


    whereclause_buids = where_clause("buid", finalbuids)
    query = f"SELECT products FROM sessions {whereclause_buids}"
    cur.execute(query)
    productlist = cur.fetchall()
    finallist = list(itertools.chain(*productlist))

    """
    nextwhereclause = whereClause(id, finallist)
    newquery = f"SELECT id FROM repeatables {nextwhereclause}"

    newresults = cur.execute(newresults)"""

    con.commit()
    cur.close()
    con.close()

    return finallist

print(getItemIDs('5a393ef6a825610001bb6c51'))