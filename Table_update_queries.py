
"""
Author: Jorn van der Ent
Script for executing queries to the groupwork database
"""

import MySQLdb
import config as cfg
import query_functies_dict
import Table_Lookup_queries as TLQ
import import_oligo_parser as iop

def execute_edit_queries(query): #works
    """ Executes queries that edit the database (insert, update, delete)
        
    Keyword Arguments:
        query -- string in a SQL query format
    """
    # open connection
    db = MySQLdb.connect(cfg.mysql['host'], cfg.mysql['user'],
                         cfg.mysql['password'], cfg.mysql['database'])
   
    cursor = db.cursor() # prepare a cursor object
    try:
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
    except MySQLdb.Error,e:# Rollback in case there is any error
        #print e[0], e[1]
        db.rollback()
        raise ValueError(e[0], e[1])
        cursor.close()
        db.close() #disconnect from server

def make_insert_row(table_str, attribute_value_dict): #works
#Aanpassen zodat query niet uitgevoerd wordt als pk al bestaat
    """Returns a insert row SQL statement in a string
        
    Keyword Arguments:
        table_str -- string, a table
        attribute_value_dict-- a dictionary, with the attribute as key and
        the value as value
    """
    #initialize input for string formatting
    attributes_string = "("
    values_list = []
    #retrieve attributes and values from dictionary and add them to the string
    for key in attribute_value_dict:
        values_list += [attribute_value_dict[key]]
        attributes_string += "%s, " % key
    attributes_string = attributes_string[:(len(attributes_string)-2)]
    attributes_string += ')'
    values = str(tuple(values_list))
    sql = """INSERT INTO `%s` %s VALUES %s """ % (table_str, attributes_string, values)
    return sql

def insert_row(table_str, attribute_value_dict): #works
    """Inserts a new row
        
    Keyword Arguments:
        table_str -- string, a table
        attribute_value_dict -- a dictionary, with the attribute as key and
        the value as value
    """
    sql = make_insert_row(table_str, attribute_value_dict)
    #print sql
    execute_edit_queries(sql)
    
def make_delete_row(table_str, key_value_dict): # works
    """Returns a delete row SQL statement in a string
        
    Keyword Arguments:
        table_str -- string, a table
        attribute_value_dict -- a dictionary, with the attribute as key and the
        value as value
    """
    
    # initialize query statement and input
    sql = """DELETE FROM `%s` WHERE %s = '%s'"""
    # create list of attributes
    attributes_list = key_value_dict.keys()
    #create list for the values
    value_list = []
    for key in attributes_list:
        value_list += [key_value_dict[key]]
    # initialize the first input (to match with the top sql-statement)
    input_format = (table_str, attributes_list[0], value_list[0])
    # add an AND to the Where-clause for multi-keys
    for i in range(1, len(attributes_list)):
        sql += " AND %s = '%s'"
        input_format += (attributes_list[i], value_list[i])
    # combine query & input, run
    sql = sql % input_format
    return sql

def delete_row(table_str, key_value_dict): #works
    """Deletes a row
        
    Keyword Arguments:
        table_str -- string, a table
        attribute_value_dict-- a dictionary, with the attribute as key and
        the value as value
    """
    sql = make_delete_row(table_str, key_value_dict)
    execute_edit_queries(sql)
    
def make_update_row(table_str, attribute_value_dict, keys_dict): #works
    """Returns an update row SQL statement in a string
        
    Keyword Arguments:
        table_str -- string, a table of the db
        attribute_value_dict -- a dictionary of the attributes you want to
        change, with the attribute as key and the value as value.
        keys_dict -- a dictionary of the (combination) primary key, with
        the attribute as key and the value as value
    """

    # initialize query statement and input
    sql = """UPDATE `%s` SET %s = '%s'"""
    # get attributes from the dictionaries and initialize list for values
    attributes_list = attribute_value_dict.keys()
    value_list = []
    list_of_key_attributes = keys_dict.keys()
    list_of_key_values = []
    # create list of values from the dictionary
    for key in attributes_list:
        value_list += [attribute_value_dict[key]]
    for key in list_of_key_attributes:
        list_of_key_values += [keys_dict[key]]
    input_format = (table_str, attributes_list[0], value_list[0])
    # add set's to the query statemtens and input
    for i in range(1, len(attributes_list)):
        sql += ", %s = '%s'"
        input_format += (attributes_list[i], value_list[i])
    # add the Where-clause
    sql += " WHERE  %s = '%s'"
    input_format += (list_of_key_attributes[0], list_of_key_values[0])
    # add an AND to the Where-clause for multi-keys
    for i in range(1, len(list_of_key_attributes)):
        sql += " AND %s = '%s'"
        input_format += (list_of_key_attributes[i], list_of_key_values[i])
    # combine query & input, run
    sql = sql % input_format
    return sql


def update_row(table_str, attribute_value_dict, keys_dict): #works
    """ Updates a row in the db
        
    Keyword Arguments:
        table_str -- string, a table
        attribute_value_dict -- a dictionary of the attributes you want to
        change, with the attribute as key and the value as value.
        keys_dict -- a dictionary of the (combination) primary key, with
        the attribute as key and the value as value
    """
    sql = make_update_row(table_str, attribute_value_dict, keys_dict)
    #print sql
    execute_edit_queries(sql)

def move_row(pk_ID, source, target): # works
    """Moves an oligo from the oligo table to the Oligo bin.

    Keyword Arguments:
        pk_ID -- string, the primary key of the row to move
        source -- string, tablename of the table the row is in
        target -- string, tablename of the table the row has to move to
    """
    db = MySQLdb.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['database']) # open connection
    cursor = db.cursor() # prepare a cursor object

    #locate the oligo in the table, retrieve values
    row = TLQ.search_in_single_attribute(source, cfg.db_tables_views[source][0], pk_ID)
    if len(row) == 0 or str(row[0][0]) != pk_ID:
        raise ValueError("Could not find ID")
    #convert to list, for indexing purposes
    row = list(row[0])
    #initialize attributes and dictionary
    attributes = cfg.db_tables_views[source]
    insertdict = {}
    #create dictionary for function inputs
    for i in range(len(attributes)):
        if row[i] == None:
            row[i] = ''
        if type(row[i]) == long:
            row[i] = float(row[i])
        insertdict[attributes[i]] = row[i]
    
    # Replace source key-attribute with target key-attribute and value
    del insertdict[cfg.db_tables_views[source][0]]
    insertdict[cfg.db_tables_views[target][0]] = iop.make_new_ID(target)
    
    # get the queries
    insert_sql = make_insert_row(target, insertdict)
    delete_sql = make_delete_row(source, {cfg.db_tables_views[source][0] : pk_ID})
    
    try:
        cursor.execute(insert_sql)
        cursor.execute(delete_sql)
        db.commit()
    except MySQLdb.Error,e: # Rollback in case there is any error
        print e[0], e[1]
        db.rollback()
    cursor.close()
    db.close() #disconnect from server

def empty_bin(): # works
    """ Empties the Order Bin.
    """

    db = MySQLdb.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['database']) # open connection
    cursor = db.cursor() # prepare a cursor object

    pkeys = TLQ.all_pks_table('order_bin')
    if len(pkeys) == 0:
        raise ValueError("Table is already empty")
    
    # per id make sql and execute deletion
    for i in range(len(pkeys)):
        delete_sql = make_delete_row('order_bin', {'bin_ID' : pkeys[i][0]})
        try:
            cursor.execute(delete_sql)
            db.commit()
        except MySQLdb.Error,e: # Rollback in case there is any error
            print e[0], e[1]
            db.rollback()
    cursor.close()
    db.close() #disconnect from server

if __name__ == "__main__":
    print ""
    #insert_row('Oligo', { 'oligo_ID' : 'OlI0012', 'oligo_name' : 'test', 'oligo_type': '', 'sequence' : 'J', 'description':'',  'entry_date':'', 'creator':'EMP0000', 'update_date':'', 'modifier':'EMP0000', 'label5prime':'', 'label3prime':'', 'labelM1':'', 'labelM1position':'', 'pathogen_name':'', 'target':'', 'notes':''})
    #delete_row('Employee', { 'employee_ID' : 'EMP0066', 'emp_name' : 'test20'})
    #update_row('Employee', { 'password' : 'test'}, { 'emp_name' : 'test'})
    #move_row(1, 'order_bin', 'order_queue')
