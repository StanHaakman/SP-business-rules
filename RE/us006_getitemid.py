from _functions._base_functions import where_clause, create_table
import itertools
import psycopg2


#class Repeatable:

def filter_list_of_strings_of_list(lijst):

    firstfilter = []
    secondfilter = []

    #kijk of de lijst een of meerdere strings bevat
    if isinstance(lijst[0], str):
        for i in range(len(lijst)):
            firstfilter.append(eval(lijst[i]))

    #kijk of de lijst een of meerdere lijsten bevat
    if isinstance(firstfilter[0], list):
        for sublist in firstfilter:
            for item in sublist:
                secondfilter.append(item)

    return secondfilter


def get_profile_buids(profileID, cur):
    """takes a profile ID and returns all buids belonging to that profile"""

    #creates and executes query
    query = f"SELECT buids FROM visitors WHERE (idvisitors = '{profileID}')"
    cur.execute(query)
    buidslist = cur.fetchall()

    #filters the buids where possible
    finallist = (list(itertools.chain(*buidslist)))
    try:
        finallist = eval(finallist[0])
    except:
        pass

    return finallist


def get_item_ID(tablevalues, tablename, valuename, valuelist, cur):
    """creates a where clause for a query, executes the query and filters the list"""

    newidlist = []
    #create the where clause and checks if string is not empty (if it is, raise exception
    whereclause = where_clause(valuename, valuelist)

    #create and execute the query
    query = f"SELECT {tablevalues} FROM {tablename} {whereclause}"
    cur.execute(query)
    idlist = cur.fetchall()

    #filter the resulting list
    finalidlist = list(itertools.chain(*idlist))

    return finalidlist


def put_in_table(profileID, recommendlist, cur):
    query = f"INSERT INTO visitorrepeatable (visitorid, recomm_one, recomm_two, recomm_three, recomm_four) VALUES ('{profileID}', {recommendlist[0]}, {recommendlist[1]}, {recommendlist[2]}, {recommendlist[3]})"

    cur.execute(query)

    return


def get_herhaal_Item_IDs(profileID):

    con = psycopg2.connect(
        host='localhost',
        password='',
        user='postgres',
        database='huwebshop'
    )
    cur = con.cursor()

    buids_list = get_profile_buids(profileID, cur)

    prod_id_list = get_item_ID("products", "sessions", "buid", buids_list, cur)

    perfectidlist = filter_list_of_strings_of_list(prod_id_list)

    recommend_id_list = get_item_ID("idproducts", "repeatables", "idproducts", perfectidlist, cur)

    put_in_table(profileID, recommend_id_list, cur)

    con.commit()
    cur.close()
    con.close()

    return


def create_repeatable_per_visitor():
    deletequery = "DROP TABLE IF EXISTS visitorrepeatable CASCADE "
    createquery = "CREATE TABLE IF NOT EXISTS visitorrepeatable (" \
                  "visitorid VARCHAR(255) NOT NULL, " \
                  "recomm_one VARCHAR(255) NOT NULL, " \
                  "recomm_two VARCHAR(255) NOT NULL, " \
                  "recomm_three VARCHAR(255) NOT NULL, " \
                  "recomm_four VARCHAR(255) NOT NULL, " \
                  "PRIMARY KEY (visitorID))"

    con = psycopg2.connect(
        host='localhost',
        password='',
        user='postgres',
        database='huwebshop'
    )
    cur = con.cursor()
    cur.execute(deletequery)
    cur.execute(createquery)
    con.commit()
    cur.close()
    con.close()

"""
def get_all_profileIDs():
    con = psycopg2.connect(
        host='localhost',
        password='',
        user='postgres',
        database='huwebshop'
    )
    cur = con.cursor()

    query = f""

    con.commit()
    cur.close()
    con.close()
"""




print(get_herhaal_Item_IDs('5a396e36a825610001bbb368'))
