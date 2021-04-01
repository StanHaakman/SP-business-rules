from recom_functions._base_functions import where_clause, or_clause
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
    con = psycopg2.connect(
        host='localhost',
        password='postgres',
        user='postgres',
        database='huwebshop'
    )
    cur = con.cursor()

    buids_list = get_profile_buids(profileID, cur)

    prod_id_list = get_item_ID("products", "sessions", "buid", buids_list, cur)

    if len(prod_id_list) < 1:
        return []
    perfectidlist = filter_list_of_strings_of_list(prod_id_list)

    recommend_id_list = get_item_ID("idproducts", "repeatables", "idproducts", perfectidlist, cur)

    for i in recommend_id_list:
        if i not in idDict.keys():
            idDict[i] = 1
        else:
            idDict[i] += 1

    #sorteer de dictionary op hoogste values
    sorted_idDict = dict(sorted(idDict.items(), key=operator.itemgetter(1), reverse=True))

    finalidlist = list(sorted_idDict.keys())

    # put_in_table(profileID, recommend_id_list, cur)

    con.commit()
    cur.close()
    con.close()

    return finalidlist[:4]


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