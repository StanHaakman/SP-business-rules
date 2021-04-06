from recom_functions._base_functions import or_clause
import operator
import itertools
import psycopg2


# class Repeatable:
def filter_list_of_strings_of_list(lst):
    firstfilter = []
    secondfilter = []

    # kijk of de lijst een of meerdere strings bevat
    if isinstance(lst[0], str):
        for i in range(len(lst)):
            firstfilter.append(eval(lst[i]))

    # kijk of de lijst een of meerdere lijsten bevat
    if isinstance(firstfilter[0], list):
        for sublist in firstfilter:
            for item in sublist:
                secondfilter.append(item)

    return secondfilter


def get_profile_buids(profileID, cur):
    """takes a profile ID and returns all buids belonging to that profile"""

    # creates and executes query
    query = f"SELECT buids FROM visitors WHERE (idvisitors = '{profileID}')"
    cur.execute(query)
    buidslist = cur.fetchall()

    # filters the buids where possible
    finallist = (list(itertools.chain(*buidslist)))
    try:
        finallist = eval(finallist[0])
    except:
        pass

    return finallist


def get_item_ID(tablevalues, tablename, valuename, valuelist, cur):
    """creates a where clause for a query, executes the query and filters the list"""

    # create the where clause and checks if string is not empty (if it is, raise exception
    whereclause = or_clause(valuename, valuelist)

    if len(whereclause) < 1:
        return []
    # create and execute the query
    query = f"SELECT {tablevalues} FROM {tablename} WHERE {'has_sale = true AND' if tablename == 'sessions' else ''} ({whereclause})"
    cur.execute(query)
    idlist = cur.fetchall()

    # filter the resulting list
    finalidlist = list(itertools.chain(*idlist))

    return finalidlist


def put_in_table(profileID, recommendlist, cur):
    query = f"INSERT INTO visitorrepeatable (visitorid, recomm_one, recomm_two, recomm_three, recomm_four) VALUES ('{profileID}', {recommendlist[0]}, {recommendlist[1]}, {recommendlist[2]}, {recommendlist[3]})"

    cur.execute(query)

    return


def get_herhaal_Item_IDs(profileID):
    idDict = {}
    finalids = []
    con = psycopg2.connect(
        host='localhost',
        password='',
        user='postgres',
        database='huwebshop'
    )
    cur = con.cursor()

    # get all user sessions
    buids_list = get_profile_buids(profileID, cur)

    # get all products user has bought
    prod_id_list = get_item_ID("products", "sessions", "buid", buids_list, cur)

    # if list is not empty, filter the list to get correct type
    if len(prod_id_list) < 1:
        return []
    perfectidlist = filter_list_of_strings_of_list(prod_id_list)

    # get all items from the repeatables products
    recommend_id_list = get_item_ID("idproducts", "repeatables", "idproducts", perfectidlist, cur)

    # put all the item ids in a dictionary with amount bought in the history
    for i in recommend_id_list:
        if i not in idDict.keys():
            idDict[i] = 1
        else:
            idDict[i] += 1

    # sort the dictionary to highest values
    sorted_idDict = dict(sorted(idDict.items(), key=operator.itemgetter(1), reverse=True))

    allrepeatables = list(sorted_idDict.keys())
    # put_in_table(profileID, recommend_id_list, cur)

    # get all items from the 100 most popular repeatables products
    toprepeatables = get_item_ID("idproducts", "popular_repeatables", "idproducts", perfectidlist, cur)

    # merge lists together
    almostidlist = toprepeatables + allrepeatables

    # filter doubles out of the list
    [finalids.append(x) for x in almostidlist if x not in finalids]

    con.commit()
    cur.close()
    con.close()

    return finalids[:4]


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
