"""
Author: Melanie van den Bosch
Script for parsing import oligos into dictionary
Script "query_functies_as_dictionary.py" puts these inside
SQL database
"""

import MySQLdb
import time
import datetime
import re
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

            ## retrieve information from the database (and convert)
            # get current date
            date = get_date_stamp()
            # make a new oligonumber
            oli_ID = make_new_ID('Oligo')
            # make new batch number
            batch_no = make_new_ID('Batch')
            # make new order number
            order_number = # function


            ## put everything in dictionaries
            # for Oligo table
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

            # for Order table
            # deze moet echter pas gecreerd worden na het processen van de oligos
            
            import_order_dict["order_date"] = date

            # for Employee table

            # for Supplier table
            import_supplier_dict["supplier_name"] = supp_name

            # for Batch table
            import_batch_dict["batch_number"] = batch_no
            import_batch_dict["synthesis_level_ordered"] = syn_lev
            import_batch_dict["purification_method"] = pur_met

           

            # for every row insert the information into the specified tables
            insert_row("Oligo", import_oli_dict)
            insert_row("Order", import_order_dict)
            insert_row("Supplier", import_supplier_dict)
            #insert_row("Employee", import_emp_dict)
            insert_row("Batch", import_batch_dict)
            

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
    if table == "order":
        sql = """SELECT MAX(order_number) FROM pathofinder_db.`%s` """%(table)
    # the sql query retuns a tuple, we only want to take the number
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
    if table == "order":
        #new_order_ID = new_order_no(table)
        

def check_uniq_sequence(seq):
    """checks whether an oligo sequence is unique or not"

    Returns:
    A boolean, true when oligo sequence is unique false when duplicated"
    """
    # if sequence == sequence in db
    # raise some frame
    # choose whether commit and it will get a new batchnumber but not a new olinumber
    # or choose to abort

    
def new_oligo_ID(table):
    """ Converts the max oligo_ID in the database to the following up ID.

    """
    # retrieve only the number part
    max_ID = get_max_ID(table)
    # retaining the same length of the oligo_ID's (6 digits)
    # 2 groups in pattern
    pattern = re.compile(r'(OLI)([0-9]+)')
    matcher = pattern.search(max_ID)
    # if matcher is found proceed
    if matcher != None:
        # split the 2 groups
        oli = matcher.group(1)
        olino = matcher.group(2)
        # convert oligo number and add 1
        int_olino = int(olino)
        new_olino = int_olino + 1
        convert_olino = str(new_olino)
        # fill in 0's up until 6 digits
        complete_olino = convert_olino.zfill(6)
        # make complete oligoID 
        new_oligoID = oli + complete_olino
        return new_oligoID


def new_batch_number(table):
    """ Converts the max batch_number in the database to the following up number.
    """
    max_ID = get_max_ID(table)
    # retrieve only variable part
    # first 4 digits are constant per year, need to be sliced off
    string_max_ID = str(max_ID)
    # search for pattern, when found proceed
    pattern = re.compile(r'([0-9][0-9][0-9][0-9])([0-9]+)')
    matcher = pattern.search(string_max_ID)
    if matcher != None:
        # split 2 groups
        year = matcher.group(1)
        batchno = matcher.group(2)
        #convert batchno and add 1
        int_batchno = int(batchno)
        new_batchno = int_batchno + 1
        convert_batchno = str(new_batchno)
        # fill in 0's up to 4 digits
        complete_batchno = convert_batchno.zfill(4)
        print complete_batchno
        # check whether year is the same, when not start over with numbering
        actual_year = get_date_stamp()[6:]
        print actual_year
        if actual_year != year:
            # start at 0001 when a new year is found
            newyear_batchno = actual_year + "0001"
            new_batch_number = int(newyear_batchno)
        else:
            thisyear_batchno = year + complete_batchno
            new_batch_number = int(string_batchno)
        return new_batch_number
        
def new_order_no(table): #does not work yet because order number is with X in db
    """ Converts the max order in the database to the following up number.
    """
    max_ID = get_max_ID(table)
    # retrieve only variable part
    # first 4 digits are constant per year, need to be sliced off
    string_max_ID = str(max_ID)
    # search for pattern, when found proceed
    pattern = re.compile(r'([0-9][0-9][0-9][0-9])(.)([0-9]+)')
    matcher = pattern.search(string_max_ID)
    if matcher != None:
        # split 2 groups
        year = matcher.group(1)
        dot = matcher.group(2)
        orderno = matcher.group(3)
        #convert batchno and add 1
        int_orderno = int(orderno)
        new_orderno = int_orderno + 1
        convert_orderno = str(new_orderno)
        # fill in 0's up to 3 digits
        complete_orderno = convert_orderno.zfill(3)
        print complete_batchno
        # check whether year is the same, when not start over with numbering
        actual_year = get_date_stamp()[6:]
        print actual_year
        if actual_year != year:
            # start at 0001 when a new year is found
            new_order_number = actual_year + dot + "0001"
        else:
            new_order_number = year + dot + complete_batchno

        return new_order_number



    

if __name__ == "__main__":
    host = '127.0.0.1'
    user = 'root'
    password = 'root'
    database = 'pathofinder_db'
