from _functions._base_functions import where_clause
import itertools
import psycopg2


def get_profile_buids(profileID, cur):
    """takes a profile ID and returns all buids belonging to that profile"""

    #creates and executes query
    buidsquery = f"SELECT buids FROM visitors WHERE (idvisitors = '{profileID}')"
    print(buidsquery)
    cur.execute(buidsquery)
    buidslist = cur.fetchall()

    #filters the buids where possible
    finalbuids = (list(itertools.chain(*buidslist)))
    try:
        finalbuids = eval(finalbuids[0])
    except:
        pass

    return finalbuids


def get_item_ID(tablevalues, tablename, valuename, valuelist, cur):
    """creates a where clause for a query, executes the query and filters the list"""

    #create the where clause and checks if string is not empty (if it is, raise exception
    whereclause = where_clause(valuename, valuelist)
    if len(whereclause) != 0:
        pass
    else:
        raise Exception("no products have been found")

    #create and execute the query
    query = f"SELECT {tablevalues} FROM {tablename} {whereclause}"
    print(query)
    cur.execute(query)
    productlist = cur.fetchall()

    #filter the resulting list
    prodidlist = list(itertools.chain(*productlist))
    try:
        prodidlist = eval(prodidlist[0])
    except:
        pass

    return prodidlist


def get_herhaal_Item_IDs(profileID):

    con = psycopg2.connect(
        host='localhost',
        password='postgres',
        user='postgres',
        database='huwebshop'
    )
    cur = con.cursor()

    finalbuids = get_profile_buids(profileID, cur)

    prodidlist = get_item_ID("products", "sessions", "buid", finalbuids, cur)

    finalidlist = get_item_ID("idproducts", "repeatables", "idproducts", prodidlist, cur)

    """
    whereclauseids = where_clause("idproducts", prodidlist)
    newquery = f"SELECT idproducts FROM repeatables {whereclauseids}"
    print(newquery)

    cur.execute(newquery)
    idlist = cur.fetchall()
    finalidlist = list(itertools.chain(*idlist))
    """

    con.commit()
    cur.close()
    con.close()

    return finalidlist

print(get_herhaal_Item_IDs('5a393ef6a825610001bb6c51'))
print(get_herhaal_Item_IDs('5a394aa8a825610001bb7aed'))