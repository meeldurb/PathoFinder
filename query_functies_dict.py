
"""
Author: Jorn van der Ent
Script for executing queries to the groupwork database
"""

import MySQLdb
import time
import datetime

####
####
####        database editing functions (insert, update, delete)
####
####

def execute_edit_queries(query): #works
    """Executes queries that edit the database somehow (insert, update, delete)
        
    Keyword Arguments:
    SQL query -- string in a SQL query format"""
    
    db = MySQLdb.connect(host, user, password, database) # open connection
    cursor = db.cursor() # prepare a cursor object
    try:
        cursor.execute(query)
        db.commit()   
    except MySQLdb.Error,e:# Rollback in case there is any error
        print e[0], e[1]
        db.rollback()
    cursor.close()
    db.close() #disconnect from server

def make_insert_row(table_str, attribute_value_dict): #works
    """Returns a insert row SQL statement in a string
        
    Keyword Arguments:
    table_str               -- string, a table
    attribute_value_dict    -- a dictionary, with the attribute as key and the value as value"""
    #initialize input for string formatting
    attributes_string = "("
    values_list = []
    #retrieve attributes and values from dictionary and add them to the string
    for key in attribute_value_dict:
        values_list += [attribute_value_dict[key]]
        attributes_string += "%s, " % key
    attributes_string = attributes_string[:(len(attributes_string)-2)]
    attributes_string += ')'
    values_tuple = tuple(values_list)
    sql = """INSERT INTO `%s` %s VALUES %s """ % (table_str, attributes_string, values_tuple)
    return sql

def insert_row(table_str, attribute_value_dict): #works
    """Inserts a new row
        
    Keyword Arguments:
    table_str               -- string, a table
    attribute_value_dict    -- a dictionary, with the attribute as key and the value as value"""
    sql = make_insert_row(table_str, attribute_value_dict)
    execute_edit_queries(sql)
    
def make_delete_row(table_str, key_value_dict): # works
    """Returns a delete row SQL statement in a string
        
    Keyword Arguments:
    table_str               -- string, a table
    attribute_value_dict    -- a dictionary, with the attribute as key and the value as value"""
    
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
    table_str               -- string, a table
    attribute_value_dict    -- a dictionary, with the attribute as key and the value as value"""
    sql = make_delete_row(table_str, key_value_dict)
    execute_edit_queries(sql)
    
def make_update_row(table_str, attribute_value_dict, keys_dict): #works
    """Returns an update row SQL statement in a string
        
    Keyword Arguments:
    table_str           -- string, a table
    attribute_value_dict    -- a dictionary of the attributes you want to change, with the attribute as key and the value as value.
    keys_dict               -- a dictionary of the (combination) primary key, with the attribute as key and the value as value"""

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
    """Updates a row
        
    Keyword Arguments:
    table_str           -- string, a table
    attribute_value_dict    -- a dictionary of the attributes you want to change, with the attribute as key and the value as value.
    keys_dict               -- a dictionary of the (combination) primary key, with the attribute as key and the value as value"""
    sql = update_row(table_str, attribute_value_dict, keys_dict)
    execute_edit_queries(sql)

def oligo_to_temp_bin(oligo_ID): # works
    """Moves an oligo from the oligo table to the Oligo bin.

    Keyword Arguments:
    oligo_ID    -- string, the key-value of the oligo you want to remove"""
    db = MySQLdb.connect(host, user, password, database) # open connection
    cursor = db.cursor() # prepare a cursor object

    #locate the oligo in the table, retrieve values
    oligo = search_in_single_attribute('Oligo', 'oligo_ID', oligo_ID)
    if len(oligo) == 0:
        raise ValueError("Could not find oligo_ID")
    #convert to list, for indexing purposes
    oligo = list(oligo[0])
    #initialize attributes and dictionary
    oligo_attributes = ['oligo_ID', 'oligo_name', 'oligo_type', 'sequence', 'description', 'entry_date', 'creator', 'update_date', 'modifier', 'label5prime', 'label3prime', 'labelM1', 'labelM1position', 'pathogen_name', 'target','notes']
    oligo_dict = {}
    #create dictionary for function inputs
    for i in range(len(oligo_attributes)):
        if oligo[i] == None:
            oligo[i] = ''
        oligo_dict[oligo_attributes[i]] = oligo[i]
    # get the queries
    insert_sql = make_insert_row('Oligo_bin', oligo_dict)
    delete_sql = make_delete_row('Oligo', {'oligo_ID' : oligo_ID})
    try:
        cursor.execute(insert_sql)
        cursor.execute(delete_sql)
        db.commit()
    except MySQLdb.Error,e: # Rollback in case there is any error
        print e[0], e[1]
        db.rollback()
    cursor.close()
    db.close() #disconnect from server


####
####
####       SELECT/Search functions
####
####


def execute_select_queries(query): #works
    """Executes select queries, so no changes are made to the database

    Keyword Arguments:
    query   -- sting, the SELECT statement to ask the database"""
    db = MySQLdb.connect(host, user, password, database)
    cursor = db.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except MySQLdb.Error,e:
        print e[0], e[1]
        db.rollback()
    cursor.close()
    db.close()
    return results

### SEARCH


def search_in_single_attribute(table_str, attribute, search_input): #works
    """Performs a search query on the database, returns all matches in a tuple

    Keyword Arguments:
    table_str       -- string, a table
    attribute       -- string, names of the attribute to search
    search_input    -- string, the word to look for"""
    sql = """SELECT * FROM %s WHERE %s REGEXP '%s'""" % (table_str, attribute, search_input)
    return execute_select_queries(sql)

def search_entire_table(table_str, attributes_list, search_input): #works
    """Performs a search query on the database, returns all matches in a tuple

    Keyword Arguments:
    table_str       -- string, a table
    attribute       -- string, names of the attributes to search
    search_input    -- string, the word to look for"""
    results = ()
    for attribute in attributes_list:
        results += search_in_single_attribute(table_str, attribute, search_input)
    return results

def search(table_str, attributes_list, search_input): # works
    """Performs a search query on the database, recognizes spaces as ANDS, returns all matches in a list

    Keyword Arguments:
    table_str       -- string, a table
    attribute       -- string, names of the attributes to search
    search_input    -- string, the words to look for"""
    search_words = str.split(search_input)
    list_searches = []
    results = []
    for word in search_words:
        list_searches += [search_entire_table(table_str, attributes_list, word)]
    for i in range(len(list_searches)):
        for j in range(len(list_searches[i])):
            if list_searches[i][j] in list_searches[i-1]:
                if list_searches[i][j] not in results:
                    results += [list_searches[i][j]]
    return results              
            


# vanaf hier moeten ze gecheckt worden met de nieuwe database (komen namelijk uit het verslag)
# oligo and batches

def join_batch_oligo(): #works
    """Returns a tuple of the join between oligo and batch"""
    
    sql = "SELECT * FROM `oligo`, `batch` WHERE `oligo`.oligo_ID = `batch`.oligo_ID"
    return execute_select_queries(sql)

def oligo_batch_info(oligo_ID): #works
    """Returns a tuple of all the batches and related information
        from the given oligo

    Keyword Arguments:
    oligo_ID    -- string, the key of the oligo for which you want retrieve the information."""

    sql =   "SELECT `oligo`.oligo_ID, batch_number, synthesis_level_ordered, synthesis_level_delivered,\
            purification_method, spec_sheet_location, order_number, delivery_date,\
            order_status FROM oligo, batch WHERE oligo.oligo_ID = batch.oligo_ID \
            AND batch.oligo_ID = '%s'" % oligo_ID
    return execute_select_queries(sql)


# Experiments analysis

def testlist_oligo(oligo_ID): #works
    """Returns a tuple of all tests in which the given oligo was used

    Keyword Arguments:
    oligo_ID    -- string, the key of the oligo for which you want retrieve the information."""
    oligo = tuple([oligo_ID]*5)
    sql = "SELECT DISTINCT experiment.experiment_ID, test_number, lab_report, experiment_date, \
            oligo_ID_fwd, oligo_ID_rev, oligo_ID_probe, oligo_ID_4, oligo_ID_5, approved_status\
            FROM experiment, approval, `lab_report`\
            WHERE experiment.experiment_ID = approval.experiment_ID\
            AND (approval.oligo_ID_fwd = '%s'\
            OR approval.oligo_ID_rev = '%s'\
            OR approval.oligo_ID_probe = '%s'\
            OR approval.oligo_ID_4 = '%s'\
            OR approval.oligo_ID_5 = '%s')" % oligo
    return execute_select_queries(sql)

def oligolist_test_results(): #works
    """Returns a tuple of a summary of the test results for all oligos"""
    sql = "SELECT DISTINCT oligo.oligo_ID, oligo_name, COUNT(IF(approved_status='approved',1,NULL))\
            AS Approved, COUNT(IF(approved_status='neutral',1,NULL)) AS Neutral,\
            COUNT(IF(approved_status='disapproved',1,NULL)) AS Disapproved,\
            ROUND((COUNT(IF(approved_status='approved',1,NULL))/\
            (COUNT(IF(approved_status='approved',1,NULL))+COUNT(IF(approved_status='disapproved',1,NULL))\
            + COUNT(IF(approved_status='neutral',1,NULL))) *100),0) AS 'Percentage of approval' \
            FROM oligo, approval WHERE (oligo.oligo_ID = approval.oligo_ID_fwd \
            OR oligo.oligo_ID = approval.oligo_ID_rev OR oligo.oligo_ID = approval.oligo_ID_probe \
            OR oligo.oligo_ID = approval.oligo_ID_4 OR oligo.oligo_ID = approval.oligo_ID_5) \
            GROUP BY oligo_ID"
    return execute_select_queries(sql)

# Supplier evaluation

def supplier_synthesis_quality(): #works
    """Query for showing the average difference in synthesis level per supplier,
    indicating its quality"""

    sql = "SELECT supplier_name, ROUND(AVG(synthesis_level_ordered - synthesis_level_delivered),2) AS Difference \
            FROM batch, `order`, supplier \
            WHERE batch.order_number = `order`.order_number \
            AND `order`.supplier_ID = supplier.supplier_ID \
            GROUP BY supplier_name"
    return execute_select_queries(sql)

def supplier_delivery_time(): # need unified entry of dates in the database, worked with test data!
    """Query for calculating the average delivery time per supplier."""
    sql = "SELECT supplier_name, avg(DATEDIFF(str_to_date(batch.delivery_date, '%d-%m-%Y'),\
            str_to_date(`order`.order_date, '%d-%m-%Y'))) As difference\
            FROM  supplier, batch, `order`\
            where batch.order_number = `order`.order_number AND `order`.supplier_ID = supplier.supplier_ID\
            Group By supplier.supplier_name;  
    return execute_select_queries(sql)

# Project and the linked oligos

def oligos_from_project(project_name): #for some weird reason it gives an ERROR: EOL while scanning string literal, at the beginning of the sql statement 
    """Query for creating a table with the oligos from the given project

    Keyword Arguments:
    project_name  -- string, the name of the project (not ID!) in the project table """

    sql = "SELECT `oligo`.oligo_ID, oligo_name, oligo_type, sequence, description,\
            entry_date, creator, update_date, modifier, label5prime,\
            label3prime, labelM1, labelM1position, notes\
            FROM oligo, project_oligo, project\
            WHERE oligo.oligo_ID = project_oligo.oligo_ID\
            AND project_oligo.project_ID = project.project_ID\
            AND project.project_name = '%s'\
            ORDER BY entry_date DESC" % project_name
    return execute_select_queries(sql)

def find_approved_oligos_for_project(project_name):
    """Query for finding which oligo sets are approved for the given project name

    Keyword Arguments:
    project_name  -- string, the name of the project (not ID!) in the project table"""
    projectnames = tuple([project_name]*2)
    sql = "SELECT experiment.experiment_date, approval.oligo_ID_fwd,\
            approval.oligo_ID_rev, approval.oligo_ID_probe\
            FROM project_oligo, project, approval, experiment, oligo\
            WHERE project.project_name = %s\
            AND project_oligo.oligo_ID = oligo.oligo_ID\
            AND oligo.oligo_ID = approval.oligo_ID_fwd\
            AND approval.approved_status = %s\
            AND approval.experiment_ID = experiment.experiment_ID\
            ORDER BY experiment.experiment_date DESC" % projectnames
    return execute_select_queries(sql)    


# date stamp


def get_date_stamp():
    """Returns a string of the current date in format DD-MM-YYYY"""
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    return date

  

if __name__ == "__main__":
    host = '127.0.0.1'
    user = 'root'
    password = 'root'
    database = 'pathofinder_db'
    #insert_row('Oligo', { 'oligo_ID' : 'OlI0012', 'oligo_name' : 'test', 'oligo_type': '', 'sequence' : 'J', 'description':'',  'entry_date':'', 'creator':'EMP', 'update_date':'', 'modifier':'EMP', 'label5prime':'', 'label3prime':'', 'labelM1':'', 'labelM1position':'', 'pathogen_name':'', 'target':'', 'notes':''})
    #delete_row('Employee', { 'employee_ID' : 'EMP0066', 'emp_name' : 'test20'})
    #update_row('Employee', { 'employee_ID' : 'EMP0066', 'emp_name' : 'test20'}, { 'employee_ID' : 'EMP0065', 'emp_name' : 'test19'})
    #print search_in_single_attribute('Employee', 'employee_ID', 'EMP0007')
    #print search_entire_table('Employee', ['employee_ID', 'emp_name'], 'EMP0063')
    #print search("Employee", ['employee_ID', 'emp_name'], "EMP 0000")
    #print search('Oligo', ['oligo_ID', 'oligo_name', 'oligo_type', '\
    #             sequence', 'description', 'entry_date', 'creator', '\
    #             update_date', 'modifier', 'label5prime', 'label3prime', '\
    #             labelM1', 'labelM1position', 'pathogen_name', 'target', 'notes'], "OLI000006")
    #oligo_to_temp_bin('OLI0013')
    #print oligo_batch_info('OLI000088')
    #print join_batch_oligo()
    #print testlist_oligo('OLI000018')
    #print oligolist_test_results()
    #print supplier_synthesis_quality()
    print oligos_from_project('something')
    
