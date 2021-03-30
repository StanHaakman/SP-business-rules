from _functions._base_functions import drop_table, create_table, get_data_query_fetchone, store_data


def GetQuery(visitorID):
    SQL_query = "select previously_recommended from visitors where idvisitors = '{}';".format(visitorID)
    data = get_data_query_fetchone(SQL_query)
    lst = list(eval(data[0]))
    #print(data,type(data))

    return lst

def freq(lst):  
    freqs = dict()
    for x in lst:
        if x not in freqs:
            freqs.update({x:1})
            pass
        else:
            freqs[x] += 1
        pass
    return freqs


def filter_freq_to_list(dict,iterator):
    lst = []

    for x in range(-1,iterator-1):
        lst.append(list(dict)[x])
        print(list(dict)[x])
        pass
    return lst


def insert_into_actiontable():

    create_table()
    pass

def Testing():
    lst = GetQuery("5a393d68ed295900010384ca")
    freqs = freq(lst)
    filtered_ids = filter_freq_to_list(freqs,2)

    print(filtered_ids)
    insert_into_actiontable(filterd_ids)
    pass

Testing()