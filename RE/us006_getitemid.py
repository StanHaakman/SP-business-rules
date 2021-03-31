from _functions._base_functions import where_clause
import itertools
import psycopg2


def get_profile_buids(profileID, cur):
    """takes a profile ID and returns all buids belonging to that profile"""

    #creates and executes query
    query = f"SELECT buids FROM visitors WHERE (idvisitors = '{profileID}')"
    print(query)
    cur.execute(query)
    list = cur.fetchall()

    #filters the buids where possible
    finallist = (list(itertools.chain(*list)))
    try:
        finallist = eval(finallist[0])
    except:
        pass

    return finallist


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
    list = cur.fetchall()

    #filter the resulting list
    finallist = list(itertools.chain(*list))
    try:
        finallist = eval(finallist[0])
    except:
        pass

    return finallist


def get_herhaal_Item_IDs(profileID):

    con = psycopg2.connect(
        host='localhost',
        password='postgres',
        user='postgres',
        database='huwebshop'
    )
    cur = con.cursor()

    buids_list = get_profile_buids(profileID, cur)

    prod_id_list = get_item_ID("products", "sessions", "buid", buids_list, cur)

    recommend_id_list = get_item_ID("idproducts", "repeatables", "idproducts", prod_id_list, cur)

    con.commit()
    cur.close()
    con.close()

    return recommend_id_list

print(get_herhaal_Item_IDs('5a393ef6a825610001bb6c51'))
print(get_herhaal_Item_IDs('5a394aa8a825610001bb7aed'))