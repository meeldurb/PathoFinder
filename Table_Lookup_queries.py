
"""
Author: Jorn van der Ent
Script for executing queries to the groupwork database
"""

import MySQLdb
from table_windows import *
import config as cfg
    
def execute_select_queries(query): #works
    """Executes select queries, so no changes are made to the database

    Keyword Arguments:
    query   -- sting, the SELECT statement to ask the database"""
    db = MySQLdb.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['database'])
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

def build_table_window(sql, attributes):
    """Builds up the table window

    Keyword Arguments
    sql         -- string, The SQL query in a string
    attributes  -- list, attributes of the table the sql refers to"""
    tk = Tk()

    ssw = Spreadsheet(tk, width=900)
    ssw.pack(side = 'bottom', expand=TRUE, fill=BOTH)
    ssw.initialise()

    toolbox = Buttons(tk)
    toolbox.pack(in_=ssw, side = 'top')
 
    db = MySQLdb.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['database'])
    cursor = db.cursor()
       
    ssw.addColumn('')
    for attribute in attributes:
        ssw.addColumn(attribute, 300, align = LEFT)
    cursor.execute(sql)
    for i in range(cursor.rowcount):
        check = Checkbutton(ssw.spreadsheet)
        row = cursor.fetchone()
        row = list(row)
        row.insert(0, check)
        row = tuple(row)
        ssw.addRow(END, row)
    cursor.close()
    db.close()

    ssw.optimiseColumns()
    ssw.show()
    tk.mainloop()

### SEARCH

def search(table_str, search_input): # works
    """Performs a search query on the database, recognizes spaces as ANDS, returns all matches in a list

    Keyword Arguments:
    table_str       -- string, a table
    search_input    -- string, the words to look for"""
    search_words = str.split(search_input)
    search_string = ""
    for word in search_words:
        search_string += "%s|" % word
        search_string = search_string[:(len(search_string)-1)]
        attributes = cfg.db_tables_views[table_str]
    query = "SELECT * FROM `%s` WHERE " % table_str
    for i in range(len(attributes)):
        if i != (len(attributes)-1):
            query += "%s REGEXP '%s' OR " % (attributes[i], search_string)
        if i == (len(attributes)-1):
            query += "%s REGEXP '%s'" % (attributes[i], search_string)
    build_table_window(query, attributes)          
            


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



def supplier_delivery_time(): # need unified entry of dates in the database, worked with test data!
    """Query for calculating the average delivery time per supplier."""
    sql = "SELECT supplier_name, avg(DATEDIFF(str_to_date(batch.delivery_date, '%d-%m-%Y'),\
            str_to_date(`order`.order_date, '%d-%m-%Y'))) As Delivery_Difference\
            FROM  supplier, batch, `order`\
            where batch.order_number = `order`.order_number AND `order`.supplier_ID = supplier.supplier_ID\
            Group By supplier.supplier_name"
    return execute_select_queries(sql)

# Project and the linked oligos

def open_table_window(table, sort_attribute = 0, sort = 'DESC'):
    """Opens a window of the selected input table"""
    if sort != 'DESC' and sort != 'ASC':
        raise ValueError("Can only sort DESC-ending or ASC-ending")
    attributes = cfg.db_tables_views[table]
    query = "SELECT `%s`." % table
    for attribute in attributes:
            query += attribute + ", "
    query = query[:(len(query)-2)] + (" FROM `%s`" % table)
    if sort_attribute == 0:
        query += " ORDER BY %s %s" % (attributes[0], sort)
    else:
        query += " ORDER BY %s %s" % (sort_attribute, sort)
    build_table_window(query, attributes)

   
            
if __name__ == "__main__":

    #search('oligo', "OLI000006")
    #print testlist_oligo('OLI000018')
    open_table_window("approval")
