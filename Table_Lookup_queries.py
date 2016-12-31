
"""
Author: Jorn van der Ent
Script for executing queries to the groupwork database
"""

import MySQLdb

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
            Group By supplier.supplier_name"
    return execute_select_queries(sql)

# Project and the linked oligos

def oligos_from_project(project_name): #works
    """Query for creating a table with the oligos from the given project

    Keyword Arguments:
    project_name    -- string, the name of the project (not ID!) in the projec table."""

    sql = "SELECT `oligo`.oligo_ID, oligo_name, oligo_type, sequence, description,\
            entry_date, creator, update_date, modifier, label5prime,\
            label3prime, labelM1, labelM1position, notes\
            FROM oligo, project_oligo, project\
            WHERE oligo.oligo_ID = project_oligo.oligo_ID\
            AND project_oligo.project_ID = project.project_ID\
            AND project.project_name = '%s'\
            ORDER BY entry_date DESC" % project_name
    return execute_select_queries(sql)

def find_approved_oligos_for_project(project_name): # works
    """Query for finding which oligo sets are approved for the given project name

    Keyword Arguments:
    project_name  -- string, the name of the project (not ID!) in the project table"""
    sql = "SELECT DISTINCT experiment.experiment_date, experiment.experiment_ID,\
            approval.oligo_ID_fwd, approval.oligo_ID_rev, approval.oligo_ID_probe,\
            approval.oligo_ID_4, approval.oligo_ID_5\
            FROM project_oligo, project, approval, experiment, oligo \
            WHERE project.project_name = '%s'\
            AND project.project_ID = project_oligo.project_ID\
            AND project_oligo.oligo_ID = oligo.oligo_ID\
            AND approval.approved_status = 'approved'\
            AND approval.experiment_ID = experiment.experiment_ID\
            AND (oligo.oligo_ID = approval.oligo_ID_fwd \
            OR oligo.oligo_ID = approval.oligo_ID_rev\
            OR oligo.oligo_ID = approval.oligo_ID_probe \
            OR oligo.oligo_ID = approval.oligo_ID_4\
            OR oligo.oligo_ID = approval.oligo_ID_5)\
            ORDER BY experiment.experiment_date DESC" % project_name
    return execute_select_queries(sql)

def build_standard_table_sql(table):
    db_tables = {
        'oligo' : (['oligo_ID', 'oligo_name', 'oligo_type',
                   'sequence', 'description', 'entry_date',
                   'creator', 'update_date', 'modifier',
                   'label5prime', 'label3prime', 'labelM1',
                   'labelM1position', 'pathogen_name', 'target', 'notes'], ['oligo']),
        'project_oligo' : (['oligo_ID', '`project_oligo`.project_ID'], ['project_oligo']),
        'project' : (['project_ID', 'project_name'], ['project']),
        'batch' : (['batch_number', 'oligo_ID', 'synthesis_level_ordered',
                   'purification_method', 'synthesis_level_delivered',
                   'spec_sheet_location', 'order_number', 'delivery_date',
                   'order_status'], ['batch']),
        'order' : (['order_number', 'supplier_ID', 'order_date', 'employee_ID'], ['order']),
        'supplier' : (['supplier_ID', 'supplier_name'], ['supplier']),
        'oligo_oder_list' : (['.oligo_orderlist_PK', 'batch_number', 'supplier_ID',
                             'oligo_ID', 'employee_ID'], ['oligo_oder_list']),
        'employee' : (['employee_ID', 'emp_name'], ['employee']),
        'lab_report' : (['lab_report_PK', 'lab_report_location'], ['lab_report']),
        'experiment' : (['experiment_ID', 'lab_report_PK', 'experiment_date'], ['experiment']),
        'approval' : (['experiment_ID', 'test_number', 'oligo_ID_fwd',
                      'oligo_ID_rev', 'oligo_ID_4', 'oligo_ID_5', 'approved_status'],
                      ['approval']),
        'oligo_bin' : (['oligo_ID', 'oligo_name', 'oligo_type',
                   'sequence', 'description', 'entry_date',
                   'creator', 'update_date', 'modifier',
                   'label5prime', 'label3prime', 'labelM1',
                   'labelM1position', 'pathogen_name', 'target', 'notes'],
                       ['oligo_bin']),
        'batches_supplier' : (['batch_number', 'oligo_ID', 'synthesis_level_ordered',
                   'purification_method', 'synthesis_level_delivered',
                   'spec_sheet_location', 'order_number', 'delivery_date',
                   'order_status', 'order_date', 'employee_ID', 'supplier_name'], ['batch', 'order', 'supplier'])
                    }

    attributes, tablenames = db_tables[table]
    query = "SELECT `%s`." % tablenames[0]
    for attribute in attributes:
            query += attribute + ", "
    query = query[:(len(query)-2)] + (" FROM `%s`" % tablenames[0])
    query += " ORDER BY %s DESC" % attributes[0]
    return (query, attributes)
            
def build_direct_sql_dict(table):
        queries_dict = {"oligo_batch" : ("SELECT oligo.oligo_ID, oligo_name, max(batch_number) AS recent_batch, order_status, oligo_type, sequence, description, entry_date, emp_name AS creator, update_date, emp_name AS modifier, label5prime, label3prime, labelM1, labelM1position, pathogen_name, target, notes \
FROM pathofinder_db.oligo, employee, batch \
WHERE creator = employee.employee_ID \
AND modifier = employee.employee_ID \
AND oligo.oligo_ID = batch.oligo_ID \
GROUP BY oligo.oligo_ID",['oligo_ID', 'oligo_name', 'recent_batch', 'order_status', 'oligo_type', 'sequence', 'description', 'entry_date', 'creator', 'update_date', 'modifier', 'label5prime', 'label3prime', 'labelM1', 'labelM1position', 'pathogen_name', 'target', 'notes']),
                    
'approval_lab_report': ("SELECT `approval`.experiment_ID, test_number, oligo_ID_fwd, \
oligo_ID_rev, oligo_ID_4, oligo_ID_5, approved_status, experiment_date, \
lab_report_location FROM `approval`, `experiment`, \
`lab_report` WHERE `approval`.experiment_ID = `experiment`.experiment_ID \
AND `lab_report`.lab_report_PK = `experiment`.lab_report_PK \
ORDER BY experiment_date DESC",
                        ['experiment_ID', 'test_number', 'oligo_ID_fwd',
                         'oligo_ID_rev', 'oligo_ID_4', 'oligo_ID_5', 'approved_status',
                         'experiment_date', 'lab_report_location']),
'batches_supplier' : ("SELECT `batch`.batch_number, oligo_ID, synthesis_level_ordered, \
purification_method, synthesis_level_delivered, spec_sheet_location, batch.order_number, \
delivery_date, order_status, order_date, emp_name AS employee, supplier_name \
FROM `batch`, `order`, `supplier`, employee \
WHERE batch.order_number = `order`.order_number \
AND `order`.supplier_ID = supplier.supplier_ID \
AND `order`.employee_ID = employee.employee_ID \
ORDER BY batch_number DESC",
                      ['batch_number', 'oligo_ID', 'synthesis_level_ordered',
                       'purification_method', 'synthesis_level_delivered',
                       'spec_sheet_location', 'order_number', 'delivery_date',
                       'order_status', 'order_date', 'employee_ID', 'supplier_name'])
}
        return queries_dict[table]

if __name__ == "__main__":
    host = '127.0.0.1'
    user = 'root'
    password = 'root'
    database = 'pathofinder_db'

    build_table_sql('batches_supplier')
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
    #print oligos_from_project('something')
    #print find_approved_oligos_for_project('something')
