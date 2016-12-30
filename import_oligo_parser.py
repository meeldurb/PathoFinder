"""
Author: Melanie van den Bosch
Script for parsing import oligos into dictionary
Script "query_functies_as_dictionary.py" puts these inside
SQL database
"""

import MySQLdb
import time
import datetime
from query_functies_dict import execute_edit_queries
from query_functies_dict import make_insert_row
from query_functies_dict import insert_row



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

##def make_insert_row(table_str, attribute_value_dict): #works
##    """Returns a insert row SQL statement in a string
##        
##    Keyword Arguments:
##    table_str               -- string, a table
##    attribute_value_dict    -- a dictionary, with the attribute as key and the value as value"""
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
    """Inserts a new row
        
    Keyword Arguments:
    table_str               -- string, a table
    attribute_value_dict    -- a dictionary, with the attribute as key and the value as value"""
    sql = make_insert_row(table_str, attribute_value_dict)
    execute_edit_queries(sql)

    
def open_oligofile(filename):
    """ Opens a file and reads it"""

    file_content = open(filename, "r")
    # oligoreader = csv.reader(file_content, delimiter=';')
    return file_content


def parse_oligofile(filename):
    """ Returns the cells of the oligo import file to a dictionary

    Keyword arguments:
        filename -- string, the filename of the import oligo file

    Returns:
        oligo_dict -- dictionary, a dictionary of the data that will be imported
        into the database
    """
    import_data = open_oligofile(filename)
    # initialize empty dictionaries
    import_oli_dict = {}
    import_batch_dict = {}
    import_supplier_dict = {}
    rowcount = 0
    # for every single row import the data into the database
    for row in import_data:
        if rowcount > 0:
            oli_ID, oli_name, oli_type, oli_seq, descr, label5, label3, \
                    labelm, labelpos, path_name, target, notes, syn_lev, \
                    pur_met, supp_name = row.strip().split(";")
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
            import_batch_dict["synthesis_level_ordered"] = syn_lev
            import_batch_dict["purification_method"] = pur_met
            import_supplier_dict["supplier_name"] = supp_name
##            print import_oli_tuple
##            import_batch_tuple = ("Batch", import_batch_dict)
##            print import_batch_tuple
##            import_supplier_tuple = ("Supplier", import_supplier_dict)
##            print import_supplier_tuple
            insert_row("Oligo", import_oli_dict)
            #insert_row("Batch", import_batch_dict)
            # does not work yet because batchno itself is empty
            insert_row("Supplier", import_supplier_dict)
            rowcount += 1
        else:
            rowcount += 1
            
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
