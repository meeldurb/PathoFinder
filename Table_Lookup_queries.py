
"""
Author: Jorn van der Ent
Script for executing queries to the groupwork database
"""

import MySQLdb
import table_windows as tw
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

def build_table_window(sql, table_str, attributes, sortattribute, sortmethod):
    """Builds up the table window

    Keyword Arguments
    sql         -- string, The SQL query in a string
    attributes  -- list, attributes of the table the sql refers to"""
    tk = tw.Tk()

    # initialze spreadsheet frame
    ssw = tw.Spreadsheet(tk, width=900)
    ssw.pack(side = 'bottom', expand=True, fill= 'both')
    ssw.initialise()

    # add the Toolbox (the buttons) frame to the winow
    toolbox = tw.Buttons(tk, sql, table_str, attributes, sortattribute, sortmethod)
    toolbox.pack(in_=ssw, side = 'top')
 
    db = MySQLdb.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'], cfg.mysql['database'])
    cursor = db.cursor()
       
    ssw.addColumn('')
    for attribute in attributes:
        ssw.addColumn(attribute, 300, align = 'left')
    cursor.execute(sql)
    for i in range(cursor.rowcount):
        check = tw.Checkbutton(ssw.spreadsheet)
        row = cursor.fetchone()
        row = list(row)
        row.insert(0, check)
        row = tuple(row)
        ssw.addRow('end', row)
    cursor.close()
    db.close()

    ssw.optimiseColumns()
    ssw.show()
    tk.mainloop()

### SEARCH

def search(table_str, search_input, sort_attribute = 0, sort = 'Descending'): # works
    """Performs a search query on the database, recognizes spaces as ANDS, returns all matches in a list

    Keyword Arguments:
    table_str       -- string, a table
    search_input    -- string, the words to look for"""

    # check for valid sort method
    if sort != 'Descending' and sort != 'Ascending':
        raise ValueError("Expected input: 'Descending' or 'Ascending'")
    if sort == 'Descending':
        sort_syntax = 'DESC'
    else:
        sort_syntax = 'ASC'

    # load attributes
    search_words = str.split(search_input)
    attributes = cfg.db_tables_views[table_str]
    if sort_attribute == 0:
        sort_attribute = attributes[0]

     # check whether sort_attribute is valid:
    if sort_attribute not in attributes:
        raise ValueError("not a valid sort attributes, choose one that is in the table")

    # build search query
    query = "SELECT * FROM `%s` WHERE" % table_str
    for j in range(len(search_words)):
        search_string = "" 
        for i in range(len(attributes)):
            if i != (len(attributes)-1):
                search_string += "%s REGEXP '%s' OR " % ( attributes[i], search_words[j])
            if i == (len(attributes)-1):
                search_string += "%s REGEXP '%s'" % (attributes[i], search_words[j])
        if j != (len(search_words)-1):
            query += " (%s) AND" % search_string
        if j == (len(search_words)-1):
            query += " (%s)" % search_string

    # add the query for ordering the table
    query += " ORDER BY %s %s" % (sort_attribute, sort_syntax)
    return(query, attributes)
            


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

def build_query_and_table(table, sort_attribute = 0, sort = 'Descending'):
    """Opens a window of the selected input table

    Keyword Aguments:
    table --string, tablename
    sort_attribute  --string, should be an attribute in the table.
                    If it is not set, it will take the first attribute of the table
    sort            --string, the sort method to use, either Ascending or Descending"""
    # check for valid sort method
    if sort != 'Descending' and sort != 'Ascending':
        raise ValueError("Expected input: 'Descending' or 'Ascending'")
    if sort == 'Descending':
        sort_syntax = 'DESC'
    else:
        sort_syntax = 'ASC'
    attributes = cfg.db_tables_views[table]
    if sort_attribute == 0:
        sort_attribute = attributes[0]

    # check whether sort_attribute is valid:
    if sort_attribute not in attributes:
        raise ValueError("not a valid sort attributes, choose one that is in the table")
    # build query
    query = "SELECT `%s`." % table
    print query
    for attribute in attributes:
            query += attribute + ", "
    print query
    query = query[:(len(query)-2)] + (" FROM `%s`" % table)
    print query
    query += " ORDER BY %s %s" % (sort_attribute, sort_syntax)
    print query

    # show the results in the window
    build_table_window(query, table, attributes, sort_attribute, sort)

   
            
if __name__ == "__main__":
    build_query_and_table("oligo_recent_batch")

