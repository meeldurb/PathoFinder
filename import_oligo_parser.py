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
import config as cfg
from Table_update_queries import *
from Table_Lookup_queries import execute_select_queries
import config as cfg

 
def open_importfile(filename):
    """ Opens a file and reads it"""

    file_content = open(filename, "r")
    return file_content

def parse_importfile(filename):
    """ Returns the cells of the oligo import excel file to a dictionary

    Keyword arguments:
        filename -- string, the filename of the import oligo file
    """
    import_data = open_importfile(filename)
    # get current date
    entry_date = get_date_stamp()
    # initialize empty dictionary
    import_dict = {}
    rowcount = 0
    # for every row in import file import data into dictionary
    for row in import_data:
        if rowcount > 0: #skips the first line with headers
            oli_name, oli_type, oli_seq, descr, label5, label3, \
                    labelm, labelpos, path_name, target, notes, syn_lev, \
                    pur_met, supp_name, proj_name = row.strip().split(";")
            # retrieve data to import also
            proj_ID = get_project_ID(proj_name)            
            supp_ID = get_supplier_ID(supp_name)

            # put information in dictionary
            # make new queue_ID and import
            queue_no = make_new_ID('Order_queue')
            import_dict["queue_ID"] = queue_no

            import_dict["oligo_name"] = oli_name
            import_dict["oligo_type"] = oli_type
            import_dict["sequence"] = oli_seq
            import_dict["description"] = descr
            import_dict["entry_date"] = entry_date
            # creator needs to be imported from the log-in
            # import_queue_dict["creator"] = emp_loggedin
            # when an update is done also needs to be imported still, not here
            import_dict["label5prime"] = label5
            import_dict["label3prime"] = label3
            import_dict["labelM1"] = labelm
            import_dict["labelM1position"] = labelpos
            import_dict["pathogen_name"] = path_name
            import_dict["target"] = target
            import_dict["notes"] = notes
            import_dict["synthesis_level_ordered"] = syn_lev
            import_dict["purification_method"] = pur_met
            import_dict["order_status"] = "not ordered"               
            import_dict["project_ID"] = proj_ID
            import_dict["project_name"] = proj_name
            import_dict["supplier_ID"] = supp_ID
            import_dict["supplier_name"] = supp_name

            yield import_dict
            import_dict = {}
            rowcount += 1
        else:
            rowcount += 1

def import_to_queue(table, filename):
    """Imports the dictionary into the mySQL database

    Keyword arguments:
        import_dict -- dictionary, the dictionary that needs to be imported to the database
        table -- string, the table the data needs to be imported in
    """
    for import_dict in parse_importfile(filename):
        insert_row(table, import_dict)
    
    #insert_row("Batch", import_batch_dict)
    #insert_row("Project_Oligo", import_projoli_dict)
    #insert_row("Project", import_project_dict)
    #insert_row("Supplier", import_supplier_dict)


def get_from_orderqueue(queue_ID_list):
    """ Retrieves information from order_queue table 

        Keyword Arguments:
            queue_ID_list -- numeric list, a list that contains the queue_ID
            of the information that we want to import in the db
        Returns:
            yields a tuple for every separate queue_ID
    """
    # open connection
    db = MySQLdb.connect(cfg.mysql['host'], cfg.mysql['user'],
                         cfg.mysql['password'], cfg.mysql['database'])
    # prepare a cursor object
    cursor = db.cursor()
    # lookup and retrieve values
    # get a boolean here, that checks which oligos were selected for processing
    # if process = selected:
    for queue_ID in queue_ID_list:
        sql = """SELECT * FROM pathofinder_db.order_queue
             WHERE queue_ID = "%s";""" %(queue_ID)
        orderqueue_tuple = execute_select_queries(sql)[0]
        yield orderqueue_tuple

def process_to_db(queue_ID_list):
    """ Processes the information from order_queue table to the db

        Keyword Arguments:
            queue_ID_list -- numeric list, a list that contains the queue_ID
            of the information that we want to import in the db

    """
    import_oli_dict = {}
    import_batch_dict = {}
    import_supplier_dict = {}
    import_project_dict = {}
    import_projoli_dict = {}
    for orderqueue_tuple in get_from_orderqueue(queue_ID_list):
        queue_ID, oli_name, oli_type, oli_seq, descr, entry_date, \
        crea, label5, label3, labelm, labelpos, path_name, target, \
        notes, syn_lev, pur_met, orderst, \
        proid, proname, supid, supname = orderqueue_tuple
        # if sequence == sequence in db, raise error/frame
        sequence_duplicated = check_sequence_duplicated(oli_seq,
                                                            label5,
                                                            label3, labelm,
                                                            labelpos)
        

        if sequece_duplicated == False:
            oli_ID = make_new_ID('Oligo')



        if sequence_duplicated[0] == True:
            # when sequence is duplicated ask user whether sure to import
            # into database, give new batchno but same olino as sequence
            import_anyway = raw_input("The sequence (with labels) is duplicated, \
                                        import anyway? The seq will get a new \
                                        batchnumber. y/n: ")
            if import_anyway == "y":
                # do not make new oligono
                oli_ID = sequence_duplicated[1]
                # 
            else:
                print "this sequence will not be imported"

            
        if sequence_duplicated[0] != True:                    
            ## retrieve information from the database (and convert)                     

            ## put everything in dictionaries to be appropriate for import
            # make a new oligonumber
            oli_ID = make_new_ID('Oligo')
            # for Oligo table
            import_oli_dict["oligo_ID"] = oli_ID
            import_oli_dict["oligo_name"] = oli_name
            import_oli_dict["oligo_type"] = oli_type
            import_oli_dict["sequence"] = oli_seq
            import_oli_dict["description"] = descr
            import_oli_dict["entry_date"] = entry_date
            # creator needs to be imported from the log-in
            # import_oli_dict["creator"] = emp_loggedin
            # when an update is done also needs to be imported still, not here
            import_oli_dict["label5prime"] = label5
            import_oli_dict["label3prime"] = label3
            import_oli_dict["labelM1"] = labelm
            import_oli_dict["labelM1position"] = labelpos
            import_oli_dict["pathogen_name"] = path_name
            import_oli_dict["target"] = target
            import_oli_dict["notes"] = notes

            # for Batch table
            # make new batch number
            batch_no = make_new_ID('Batch')
            import_batch_dict["batch_number"] = batch_no
            import_batch_dict["oligo_ID"] = oli_ID
            import_batch_dict["synthesis_level_ordered"] = syn_lev
            import_batch_dict["purification_method"] = pur_met
            import_batch_dict["order_status"] = "not ordered"

            # for Employee table
            # Employee table is already filled, just need to transfer
            # when importing/updating

            # for project_oligo table
            import_projoli_dict["oligo_ID"] = oli_ID
            proj_ID = get_project_ID(proj_name)
            import_projoli_dict["project_ID"] = proj_ID
                
            # for project table
            proj_ID = get_project_ID(proj_name)
            import_project_dict["project_ID"] = proj_ID
            import_project_dict["project_name"] = proj_name

            # for Supplier table
            supp_ID = get_supplier_ID(supp_name)
            import_supplier_dict["supplier_ID"] = supp_ID
            import_supplier_dict["supplier_name"] = supp_name

    
def old_parse_importfile(filename): #need to split in parsing and importing
    """ Returns the cells of the oligo import file to a dictionary and import into sql database

    Keyword arguments:
        filename -- string, the filename of the import oligo file
    """
    import_data = open_importfile(filename)
    # get current date
    entry_date = get_date_stamp()
    # initialize empty dictionaries
    import_oli_dict = {}
    import_batch_dict = {}
    import_supplier_dict = {}
    import_project_dict = {}
    import_projoli_dict = {}
    # keep a rowcount, because first row with headers needs to be excluded
    rowcount = 0
    # for every single row import the data into the correct dictionaries
    for row in import_data:
        if rowcount > 0:
            oli_name, oli_type, oli_seq, descr, label5, label3, \
                    labelm, labelpos, path_name, target, notes, syn_lev, \
                    pur_met, supp_name, proj_name = row.strip().split(";")
            # if sequence == sequence in db, raise error/frame
            sequence_duplicated = check_sequence_duplicated(oli_seq,
                                                            label5,
                                                            label3, labelm,
                                                            labelpos)
            print sequence_duplicated
            if sequence_duplicated[0] == True:
                # when sequence is duplicated ask user whether sure to import
                # into database, give new batchno but same olino as sequence
                import_anyway = raw_input("The sequence (with labels) is duplicated, \
                                            import anyway? The seq will get a new \
                                            batchnumber. y/n: ")
                if import_anyway == "y":
                    # do not make new oligono
                    oli_ID = sequence_duplicated[1]
                    # Batch table
                    # make new batch number
                    batch_no = make_new_ID('Batch')
                    import_batch_dict["batch_number"] = batch_no
                    import_batch_dict["oligo_ID"] = oli_ID
                    import_batch_dict["synthesis_level_ordered"] = syn_lev
                    import_batch_dict["purification_method"] = pur_met
                    import_batch_dict["order_status"] = "not ordered"

                    # for Employee table
                    # Employee table is already filled, just need to transfer
                    # when importing/updating

                    # for project_oligo table
                    import_projoli_dict["oligo_ID"] = oli_ID
                    proj_ID = get_project_ID(proj_name)
                    import_projoli_dict["project_ID"] = proj_ID
                    
                    # for project table
                    import_project_dict["project_ID"] = proj_ID
                    import_project_dict["project_name"] = proj_name

                    # for Supplier table
                    supp_ID = get_supplier_ID(supp_name)
                    import_supplier_dict["supplier_ID"] = supp_ID
                    import_supplier_dict["supplier_name"] = supp_name

                    insert_row("Oligo", import_oli_dict)
                    insert_row("Batch", import_batch_dict)
                    insert_row("Project_Oligo", import_projoli_dict)
                    insert_row("Project", import_project_dict)
                    insert_row("Supplier", import_supplier_dict)
                else:
                    rowcount += 1             
                
            if sequence_duplicated[0] != True:                    
                ## retrieve information from the database (and convert)                     

                ## put everything in dictionaries to be appropriate for import
                # make a new oligonumber
                oli_ID = make_new_ID('Oligo')
                # for Oligo table
                import_oli_dict["oligo_ID"] = oli_ID
                import_oli_dict["oligo_name"] = oli_name
                import_oli_dict["oligo_type"] = oli_type
                import_oli_dict["sequence"] = oli_seq
                import_oli_dict["description"] = descr
                import_oli_dict["entry_date"] = entry_date
                # creator needs to be imported from the log-in
                # import_oli_dict["creator"] = emp_loggedin
                # when an update is done also needs to be imported still, not here
                import_oli_dict["label5prime"] = label5
                import_oli_dict["label3prime"] = label3
                import_oli_dict["labelM1"] = labelm
                import_oli_dict["labelM1position"] = labelpos
                import_oli_dict["pathogen_name"] = path_name
                import_oli_dict["target"] = target
                import_oli_dict["notes"] = notes

                # for Batch table
                # make new batch number
                batch_no = make_new_ID('Batch')
                import_batch_dict["batch_number"] = batch_no
                import_batch_dict["oligo_ID"] = oli_ID
                import_batch_dict["synthesis_level_ordered"] = syn_lev
                import_batch_dict["purification_method"] = pur_met
                import_batch_dict["order_status"] = "not ordered"

                # for Employee table
                # Employee table is already filled, just need to transfer
                # when importing/updating

                # for project_oligo table
                import_projoli_dict["oligo_ID"] = oli_ID
                proj_ID = get_project_ID(proj_name)
                import_projoli_dict["project_ID"] = proj_ID
                    
                # for project table
                proj_ID = get_project_ID(proj_name)
                import_project_dict["project_ID"] = proj_ID
                import_project_dict["project_name"] = proj_name

                # for Supplier table
                supp_ID = get_supplier_ID(supp_name)
                import_supplier_dict["supplier_ID"] = supp_ID
                import_supplier_dict["supplier_name"] = supp_name
                
            
##              yield import_oli_dict, import_batch_dict, import_projoli_dict,
##              import_project_dict, import_supplier_dict, import_employee_dict                
##              import_oli_dict = {}
##              import_batch_dict = {}
##              import_projoli_dict = {}
##              import_project_dict = {}
##              import_supplier_dict = {}
##              import_employee_dict = {}



                # for every row insert the information into the specified tables
                # for import_oli_dict, import_supplier_dict, import_batch_dict in parse_importfile(filename)
            
                insert_row("Oligo", import_oli_dict)
                insert_row("Batch", import_batch_dict)
                insert_row("Project_Oligo", import_projoli_dict)
                insert_row("Project", import_project_dict)
                insert_row("Supplier", import_supplier_dict)
                #insert_row("Order", import_order_dict)
                #insert_row("Employee", import_emp_dict)
                
                
            

                rowcount += 1
        else:
            rowcount += 1





# for Order table
# deze moet echter pas gecreerd worden na het processen van de oligos
# import_order_dict["order_number"] = order_number
# import_order_dict["order_date"] = date

    #import_order_dict = {}
       # make new order number
    #order_number = make_new_ID('Order')
 # for Order table
            # import_order_dict["order_number"] = order_number
            # supplier_ID is taken from Supplier table
            # order_date is entered when ordered
            # employee_ID is for later when reaching to using log ins
            
def get_date_stamp():
    """Returns a string of the current date in format DD-MM-YYYY
    """
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    return date

def get_supplier_ID(supplier_name): # not sure whether need to use
    """Returns the supplier ID of a supplier_name

    Keyword arguments:
        supplier_name -- string, the name of supplier as in sql database
    Returns:
        supplier_ID -- string, the ID of supplier associated to supplier_name
    """

    sql = """SELECT supplier_ID FROM pathofinder_db.supplier
             WHERE supplier_name = "%s";""" %(supplier_name)
    supplier_tuple = execute_select_queries(sql)
    if supplier_tuple:
        supplier_ID = supplier_tuple[0][0]
        return supplier_ID
    else:
        print 'supplier is not in db. Please ask admin to import \
                supplier name and ID first'


def get_project_ID(project_name):
    """Returns the project ID of a project_name

    Keyword arguments:
        project_name -- string, the name of project as in sql database
    Returns:
        project_ID -- string, the ID of project associated to project_name
    """
    sql = """SELECT project_ID FROM pathofinder_db.project
             WHERE project_name = "%s";""" %(project_name)
    project_tuple = execute_select_queries(sql)
    if project_tuple:
        project_ID = project_tuple[0][0]
        return project_ID
    else:
        print 'project is not in db. Please ask admin to import \
                new project name and ID first'
        
    
def check_sequence_duplicated(seq, fiveprime='', threeprime='', M1='', M1pos=''):
    # fix to get information from import_oli_dict
    """checks whether an oligo sequence plus its labels is unique"

    Keyword arguments:
        seq -- the sequence that we want to import into database
        fiveprime -- the label at 5' of sequence that we want to import into db
        threeprime -- the label at 3' of sequence that we want to import into db
        M1 -- the internal label of sequence that we want to import into db
        M1pos -- the position of internal label of sequence that we want to import into db
    Returns:
        duplicated -- A boolean, False when oligo sequence is unique and True when duplicated
        oligoID -- a string, the oligoID of duplicated seq, empty when seq is unique
    """
    # from import_oli_dict the info is obtained
    # and read into seq, fiveprime, threeprime and M1, M1pos
    
    # if sequence == sequence in db
    # raise some frame
    # choose whether commit and it will get a new batchnumber but not a new olinumber
    # or choose to abort
    sql = """SELECT sequence, oligo_ID FROM pathofinder_db.oligo WHERE
            sequence = "%s" """ %(seq)
    seq_tuple = execute_select_queries(sql)
    print seq_tuple
    # not unpacking tuple yet, just checking whether something is inside
    if seq_tuple:
        # we need to retrieve also oligoID for when user wants to re-order oligo
        # the oligo gets a new batch, but keeps the oligoID
        sequence, oligoID = seq_tuple[0]
        # when tuple is filled, means that sequence is inside database
        # we also need to check whether the labels are the same 
        if check_labels_duplicated(seq, fiveprime, threeprime, M1, M1pos):
            duplicated = True
            print "sequence and labels duplicated"
        else:
            duplicated = False
            print "only sequence duplicated labels not"
    else:
        # when tuple is found empty, we can proceed importing the oligo
        duplicated = False
        oligoID = ""
        print "sequence unique"

    return duplicated, oligoID

def check_labels_duplicated(seq, fiveprime='', threeprime='', M1='', M1pos=''):
    """ Checks whether the imported labels of a sequence are equal
    to the already existing labels 

    Keyword arguments:
        seq -- the sequence that we want to import into database
        fiveprime -- the label at 5' of sequence that we want to import into db
        threeprime -- the label at 3' of sequence that we want to import into db
        M1 -- the internal label of sequence that we want to import into db
        M1pos -- the position of internal label of sequence that we want to import into db
    Returns:
        duplicated -- boolean, True when the labels are duplicated, false when unique
    """

    sql = """SELECT sequence, label5prime, label3prime, labelM1, labelM1position
        FROM pathofinder_db.oligo WHERE sequence = "%s" """ %(seq)
    
   
    sequence, labelfive, labelthree, labelM1, labelM1pos = execute_select_queries(sql)[0]
    
    print execute_select_queries(sql)
    
    if (
            fiveprime == labelfive and threeprime == labelthree and
            M1pos == labelM1pos 

        ): 
        duplicated = True
        print "labels are duplicated"
    else:
        duplicated = False
        print "unique labels"

    return duplicated




def get_max_ID(table):
    """ Retrieves the maximum ID from a table as a string from the SQL database

    Keyword Arguments:
        table -- string, the name of the table that information need to be taken from
    """
    # when a typo occurs in table naming
    table = table.lower()
    # makes a choice between which table is selected
    sql = """SELECT MAX(%s) FROM pathofinder_db.%s """ % (cfg.db_tables_views[table][0], table)
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
        new_order_ID = new_order_no(table)
    if table == "order_queue":
        new_queue_ID = new_queue_no(table)
        return new_queue_ID
    if table == 'employee':
        new_emp_ID = new_emp_ID(table)
        return new_emp_ID

def new_queue_no(table):
    """ Converts the max queue_ID in the database to the following up ID.
        When no queue it starts with 1

    Keyword Arguments:
        table -- string, the name of the table that information need to be taken from
    Returns:
        A new queue ID number
    """
    max_ID = get_max_ID(table)
    if max_ID:
        int_queueno = int(max_ID)
        new_queueno = int_queueno + 1
        new_queue_ID = str(new_queueno)
    else:
        new_queue_ID = "1"
    return new_queue_ID
        
    
def new_oligo_ID(table):
    """ Converts the max oligo_ID in the database to the following up ID.

    Keyword Arguments:
        table -- string, the name of the table that information need to be taken from
    Returns:
        A new oligo ID number
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

    Keyword Arguments:
        table -- string, the name of the table that information need to be taken from
    Returns:
        A new oligo batch number
    """
    max_ID = get_max_ID(table)
    # retrieve only variable part
    # first 4 digits are constant per year, need to be sliced off
    string_max_ID = str(max_ID)
    pattern = re.compile(r'([0-9][0-9][0-9][0-9])([0-9]+)')
    matcher = pattern.search(string_max_ID)
    # search for pattern, when found proceed
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
        # check whether year is the same, when not start over with numbering
        actual_year = get_date_stamp()[6:]
        if actual_year != year:
            # start at 0001 when a new year is found
            newyear_batchno = actual_year + "0001"
            new_batch_number = int(newyear_batchno)
        else:
            thisyear_batchno = year + complete_batchno
            new_batch_number = int(thisyear_batchno)
        return new_batch_number
        
def new_order_no(table): #should only create one per import
    # optional function is to make it work per supplier
    """ Converts the max order no to a new orderno, does this only once
    per import file

    Keyword Arguments:
        table -- string, the name of the table that information need to be taken from
    Returns:
        A new order number
    
    """
    max_ID = get_max_ID(table)
    # retrieve only variable part
    # first 4 digits are constant per year, need to be sliced off
    string_max_ID = str(max_ID)
    # search for pattern, when found proceed
    pattern = re.compile(r'ORDNO([0-9][0-9][0-9][0-9])([0-9]+)')
    matcher = pattern.search(string_max_ID)
    if matcher != None:
        # split 2 groups
        ordno = matcher.group(1)
        year = matcher.group(2)
        orderno = matcher.group(3)
        #convert batchno and add 1
        int_orderno = int(orderno)
        new_orderno = int_orderno + 1
        convert_orderno = str(new_orderno)
        # fill in 0's up to 3 digits
        complete_orderno = convert_orderno.zfill(3)
        # check whether year is the same, when not start over with numbering
        actual_year = get_date_stamp()[6:]
        if actual_year != year:
            # start at 0001 when a new year is found
            new_order_number = ordno + actual_year + "0001"
        else:
            new_order_number = ordno + year + complete_orderno

        return new_order_number

def new_emp_ID(table):
    """ Converts the max employee_ID in the database to the following up ID.

    Keyword Arguments:
        table -- string, the name of the table that information need to be taken from
    Returns:
        A new employee ID number
    """
    # retrieve only the number part
    max_ID = get_max_ID(table)
    # retaining the same length of the oligo_ID's (6 digits)
    # 2 groups in pattern
    pattern = re.compile(r'(EMP)([0-9]+)')
    matcher = pattern.search(max_ID)
    # if matcher is found proceed
    if matcher != None:
        # split the 2 groups
        emp = matcher.group(1)
        empno = matcher.group(2)
        # convert oligo number and add 1
        int_empno = int(empno)
        new_empno = int_empno + 1
        convert_empno = str(new_empno)
        # fill in 0's up until 6 digits
        complete_empno = convert_empno.zfill(4)
        # make complete oligoID 
        new_empID = emp + complete_empno
        return new_empID

if __name__ == "__main__":
##    new_batch_number("batch")
##    get_supplier_ID("IDT")
##    new_batch_number("batch")
##    dicts = parse_importfile("Importfileoligos_new.csv")
##    for i in dicts:
##        print(i)
##    import_to_queue("order_queue", "Importfileoligos_new.csv")
    #get_from_orderqueue([1,2,3,4,5])
    #process_to_db([1,2,3,4,5,6,7,8,9])


    #test1=check_sequence_duplicated("AATCACGAGGACCAAAGCACTGAATAACATTTTCCTCTCTGGTAGGGG")
    #test2=check_sequence_duplicated("AATCATCATGCCTCTTACGAGTG")
    #print test1
    #print test2
##    print type(test1[0])
##    print type(test1[1])
##    print type(test2[0])
##    print type(test2[1])
    
##    # these do not work yet as it finds 2 sequences
##    check_sequence_duplicated('TTTCCCTTCCTAACCTGGACATA', 'FAM', '', 'TAMRA', '23')
##    check_sequence_duplicated('TTTCCCTTCCTAACCTGGACATA', 'YY', 'BHQ1', 'TAMRA', '23')
##    check_sequence_duplicated('TTTCCCTTCCTAACCTGGACAT', 'FAM', '', 'TAMRA', '23')
##    check_sequence_duplicated('TTTCCCTTCCTAACCTGGACAT', 'YY', 'BHQ1', 'TAMRA', '23')

    print new_emp_ID('employee')
