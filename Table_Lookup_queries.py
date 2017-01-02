
"""
Author: Jorn van der Ent
Script for executing queries to the groupwork database
"""

import MySQLdb
from table_windows import *


db_tables_views = { #dictionary containing all tables and table-views and their attributes
    'oligo' : ['oligo_ID', 'oligo_name', 'oligo_type',
                   'sequence', 'description', 'entry_date',
                   'creator', 'update_date', 'modifier',
                   'label5prime', 'label3prime', 'labelM1',
                   'labelM1position', 'pathogen_name', 'target', 'notes'], 
    'project_oligo' : ['oligo_ID', '`project_oligo`.project_ID'], 
    'project' : ['project_ID', 'project_name'], 
    'batch' : ['batch_number', 'oligo_ID', 'synthesis_level_ordered',
                   'purification_method', 'synthesis_level_delivered',
                   'spec_sheet_location', 'order_number', 'delivery_date',
                   'order_status'],
    'order' : ['order_number', 'supplier_ID', 'order_date', 'employee_ID'],
    'supplier' : ['supplier_ID', 'supplier_name'],
    'oligo_oder_list' : ['.oligo_orderlist_PK', 'batch_number', 'supplier_ID',
                             'oligo_ID', 'employee_ID'],
    'employee' : ['employee_ID', 'emp_name'],
    'lab_report' : ['lab_report_PK', 'lab_report_location'],
    'experiment' : ['experiment_ID', 'lab_report_PK', 'experiment_date'],
    'approval' : ['experiment_ID', 'test_number', 'oligo_ID_fwd',
                      'oligo_ID_rev', 'oligo_ID_probe', 'oligo_ID_4', 'oligo_ID_5', 'approved_status'],
    'oligo_bin' : ['oligo_ID', 'oligo_name', 'oligo_type',
                   'sequence', 'description', 'entry_date',
                   'creator', 'update_date', 'modifier',
                   'label5prime', 'label3prime', 'labelM1',
                   'labelM1position', 'pathogen_name', 'target', 'notes'],
    'batches_supplier' : ['batch_number', 'oligo_ID', 'synthesis_level_ordered',
                   'purification_method', 'synthesis_level_delivered',
                   'spec_sheet_location', 'order_number', 'delivery_date',
                   'order_status', 'order_date', 'employee', 'supplier_name'],
    "oligo_batch" : ['oligo_ID', 'oligo_name', 'recent_batch', 'order_status',
                         'oligo_type', 'sequence', 'description', 'entry_date',
                         'creator', 'update_date', 'modifier', 'label5prime',
                         'label3prime', 'labelM1', 'labelM1position',
                         'pathogen_name', 'target', 'notes'],
    'approval_lab_report' : ['experiment_ID', 'test_number', 'oligo_ID_fwd',
                             'oligo_ID_rev', 'oligo_ID_4', 'oligo_ID_5',
                             'approved_status', 'experiment_date', 'lab_report_location'],
    'oligolist_test_results' : ['oligo_ID', 'oligo_name', 'Approved', 'Neutral',
                                'Disapproved', 'Percentage_of_approval'],
    'supplier_synthesis_quality': ['supplier_name', 'Synthesis_Difference'],
    'approved_oligos_for_project' : ['project_name', 'experiment_date', 'experiment_ID',
            'oligo_ID_fwd', 'oligo_ID_rev', 'oligo_ID_probe',
            'oligo_ID_4', 'oligo_ID_5'],
    'oligos_from_project': ['oligo_ID', 'oligo_name', 'oligo_type', 'sequence', 'description',
            'entry_date', 'creator', 'update_date', 'modifier', 'label5prime',
            'label3prime', 'labelM1', 'labelM1position', 'notes']
                    }
    
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
 
    db = MySQLdb.connect(host, user, password, database)
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
        attributes = db_tables_views[table_str]
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
    attributes = db_tables_views[table]
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
    host = '127.0.0.1'
    user = 'root'
    password = 'root'
    database = 'pathofinder_db'

    #search('oligo', "OLI000006")
    #print testlist_oligo('OLI000018')
    open_table_window("approval")
