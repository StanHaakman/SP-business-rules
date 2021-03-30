import RE.classes
import itertools



def getItemIDs(profileID):

    con = connect_to_db()
    cur = con.cursor()

    whereclause = whereClause(buid, buidslist)

    query = f"SELECT products FROM sessions {whereclause}"

    results = cur.execute(query)
    finallist = list(itertools.chain(*results))

    """optie 2: query met where clause id's van"""
    nextwhereclause(id, finallist)
    newquery = f"SELECT id FROM repeatables {nextwhereclause}"

    con.commit()
    con.close()
    return

