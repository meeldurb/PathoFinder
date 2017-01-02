"""
Author: Melanie van den Bosch
Script for parsing import oligos into dictionary
Script "query_functies_as_dictionary.py" puts these inside
SQL database
"""

import MySQLdb
import time
import datetime
from query_functies_dict import *
from Table_Lookup_queries import *

def execute_select_queries(query): #works
    """Executes select queries, so no changes are made to the database

    Keyword Arguments:
    query   -- string, the SELECT statement to ask the database
    """
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

def execute_edit_queries(query): #works
    """Executes queries that edit the database (insert, update, delete)
        
    Keyword Arguments:
        SQL query -- string, in a SQL query format
    """
    
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

##def make_insert_row(table_str, attribute_value_dict): #works
##    """Returns a insert row SQL statement in a string
##        
##    Keyword Arguments:
##        table_str -- string, a table
##        attribute_value_dict -- dictionary, with the attribute as key
##        and the value as value
##    """
##    #initialize input for string formatting
##    attributes_string = "("
##    values_list = []
##    #retrieve attributes and values from dictionary and add them to the string
##    for key in attribute_value_dict:
##        values_list += [attribute_value_dict[key]]
##        attributes_string += "%s, " % key
##    attributes_string = attributes_string[:(len(attributes_string)-2)]
##    attributes_string += ')'
##    values_tuple = tuple(values_list)
##    sql = """INSERT INTO `%s` %s VALUES %s """ % (table_str, attributes_string, values_tuple)
##    return sql

def insert_row(table_str, attribute_value_dict): #works
    """Inserts a new row in the database
        
    Keyword Arguments:
        table_str -- string, a table in the database
        attribute_value_dict    -- dictionary, with the attribute as key
        and the value as value
    """
    sql = make_insert_row(table_str, attribute_value_dict)
    execute_edit_queries(sql)

    
def open_importfile(filename):
    """ Opens a file and reads it"""

    file_content = open(filename, "r")
    # oligoreader = csv.reader(file_content, delimiter=';')
    return file_content


def parse_importfile(filename): #maybe need to split in parsing and importing
    """ Returns the cells of the oligo import file to a dictionary and imports
    these into the sql database

    Keyword arguments:
        filename -- string, the filename of the import oligo file
    """
    import_data = open_importfile(filename)
    # initialize empty dictionaries
    import_oli_dict = {}
    import_batch_dict = {}
    import_supplier_dict = {}
    import_order_dict = {}
    
    rowcount = 0
    # for every single row import the data into the database
    for row in import_data:
        if rowcount > 0:
            oli_name, oli_type, oli_seq, descr, label5, label3, \
                    labelm, labelpos, path_name, target, notes, syn_lev, \
                    pur_met, supp_name = row.strip().split(";")
            # if sequence exists it must not take a new oli_ID, but a new batchno
            """still have to write"""

            # first make a new oligonumber
            oli_ID = make_new_ID('Oligo')
            # put everything in dictionaries
            import_oli_dict["oligo_ID"] = oli_ID
            import_oli_dict["oligo_name"] = oli_name
            import_oli_dict["oligo_type"] = oli_type
            import_oli_dict["sequence"] = oli_seq
            import_oli_dict["description"] = descr
            import_oli_dict["label5prime"] = label5
            import_oli_dict["label3prime"] = label3
            import_oli_dict["labelM1"] = labelm
            import_oli_dict["labelM1position"] = labelpos
            import_oli_dict["pathogen_name"] = path_name
            import_oli_dict["target"] = target
            import_oli_dict["notes"] = notes

            # make new batch number
            batch_no = make_new_ID('Batch')
            import_batch_dict["batch_number"] = batch_no
            import_batch_dict["synthesis_level_ordered"] = syn_lev
            import_batch_dict["purification_method"] = pur_met
            import_supplier_dict["supplier_name"] = supp_name

            # for every row insert the information into the specified tables
            insert_row("Oligo", import_oli_dict)
            insert_row("Batch", import_batch_dict)
            insert_row("Supplier", import_supplier_dict)

            rowcount += 1
        else:
            rowcount += 1

def get_date_stamp():
    """Returns a string of the current date in format DD-MM-YYYY
    """
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    return date

def get_max_ID(table):
    """ Retrieves the maximum ID from a table as a string from the SQL database

    Keyword Arguments:
        table -- string, the name of the table that information need to be taken from
    """
    # when a typo occurs in table naming
    table = table.lower()
    # makes a choice between which table is selected
    if table == "oligo":
        sql = """SELECT MAX(oligo_ID) FROM pathofinder_db.%s """%(table)
    if table == "batch":
        sql = """SELECT MAX(batch_number) FROM pathofinder_db.%s """%(table)
    # the sql query retuns a tuple, we only want to take the OLI number
    max_ID = execute_select_queries(sql)[0][0]
    return max_ID

def make_new_ID(table):
    """ Returns a new numerical ID regarding on which table is called

    Keyword Arguments:
        table -- string, the name of the table that information need to be taken from
    Returns:
        depending on the table parameter, it calls the function for making a new
        follow up ID.
    """
    # when a typo occurs in table naming
    table = table.lower()
    # different methods for different tables
    if table == "oligo":
        new_oli_ID = new_oligo_ID(table)
        return new_oli_ID
    if table == "batch":
        new_batch_ID = new_batch_number(table)
        return new_batch_ID
        

def new_oligo_ID(table):
    """ Converts the max oligo_ID in the database to the following up ID.

    """
    # retrieve only the number part
    max_ID = get_max_ID(table)
    digit_string = max_ID.partition("OLI")[2]
    # convert to integer add 1 and convert to string again
    digits = int(digit_string)
    new_digit = digits + 1
    new_digit_string = str(new_digit)
    # add part of oligoID that is missing
    new_oligoID = "OLI" + new_digit_string
    return new_oligoID

def new_batch_number(table):
    """ Converts the max batch_number in the database to the following up number.
    """
    max_ID = get_max_ID(table)
    # retrieve only variable part
    # first 4 digits are constant per year, need to be sliced off
    str_digit = str(max_ID)
    variable_part = str_digit[4:]
    year_part = str_digit[0:4]
    print year_part
    # convert string to int and add 1
    digits = int(variable_part)
    new_digit = digits + 1
    new_digit_string = str(new_digit)
    # it omits the 0's, therefore make sure that the variable part
    # contains 4 digits
    if len(new_digit_string) < 4:
        new_digit_string = "0" + new_digit_string
    # do not take old part but look up year and add that to batchno
    year = get_date_stamp()[6:]
    # if a new year is found, start over with numbering
    if year != year_part:
        # start at 0001
        string_batch_number = year + "0001"
        new_batch_number = int(string_batch_number)
    else: 
        string_batch_number = year + new_digit_string
        new_batch_number = int(string_batch_number)
    return new_batch_number


    

if __name__ == "__main__":
    host = '127.0.0.1'
    user = 'root'
    password = 'root'
    database = 'pathofinder_db'
