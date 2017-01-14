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
from Table_update_queries import *
from Table_Lookup_queries import execute_select_queries


 
def open_importfile(filename):
    """ Opens a file and reads it"""

    file_content = open(filename, "r")
    return file_content


def parse_importfile(filename): #need to split in parsing and importing
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
    # keep a rowcount, because first row with headers needs to be excluded
    rowcount = 0
    # for every single row import the data into the correct dictionaries
    for row in import_data:
        if rowcount > 0:
            oli_name, oli_type, oli_seq, descr, label5, label3, \
                    labelm, labelpos, path_name, target, notes, syn_lev, \
                    pur_met, supp_name, proj_name = row.strip().split(";")
            
            # first check whether oli_seq is not already inside database.
            # when there is, we only need to make a new batchno
            # sometimes they also order the same seq again, but then as probe
            # need to keep in mind
            #if check_sequence_duplicated() == True:
            ## retrieve information from the database (and convert)
            
            
            # make a new oligonumber
            oli_ID = make_new_ID('Oligo')
            # make new batch number
            batch_no = make_new_ID('Batch')
            

            ## put everything in dictionaries
            # for Oligo table
            import_oli_dict["oligo_ID"] = oli_ID
            import_oli_dict["oligo_name"] = oli_name
            import_oli_dict["oligo_type"] = oli_type
            import_oli_dict["sequence"] = oli_seq
            import_oli_dict["description"] = descr
            import_oli_dict["entry_date"] = entry_date
            # creator needs to be imported from the log-in
            # when an update is done also needs to be imported still, not here
            import_oli_dict["label5prime"] = label5
            import_oli_dict["label3prime"] = label3
            import_oli_dict["labelM1"] = labelm
            import_oli_dict["labelM1position"] = labelpos
            import_oli_dict["pathogen_name"] = path_name
            import_oli_dict["target"] = target
            import_oli_dict["notes"] = notes

            # for Employee table
            # Employee table is already filled, just need to transfer
            # when importing/updating
            
            # for Supplier table
            import_supplier_dict["supplier_name"] = supp_name
            supp_ID = get_supplier_ID(supp_name)
            print supp_ID
            #import_supplier_dict["supplier_ID"] = supp_ID
            # need to keep in mind that ID is also imported, or linked
            
            # for Batch table
            import_batch_dict["batch_number"] = batch_no
            import_batch_dict["oligo_ID"] = oli_ID
            import_batch_dict["synthesis_level_ordered"] = syn_lev
            import_batch_dict["purification_method"] = pur_met
            import_batch_dict["order_status"] = "not ordered"

            # if sequence exists it must not take a new oli_ID, but a new batchno
            # still have to write

            
##            yield import_oli_dict, import_supplier_dict, import_batch_dict
##            import_oli_dict = {}
##            import_supplier_dict = {}
##            import_batch_dict = {}


            # for every row insert the information into the specified tables
            # for import_oli_dict, import_supplier_dict, import_batch_dict in parse_importfile(filename)
            
            insert_row("Oligo", import_oli_dict)
            insert_row("Supplier", import_supplier_dict)
            #insert_row("Order", import_order_dict)
            #insert_row("Employee", import_emp_dict)
            insert_row("Batch", import_batch_dict)
            

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
        supplier_name: string, the name of supplier as in sql database
    Returns:
        supplier_ID: string, the ID of supplier associated to supplier_name
    """

    sql = """SELECT supplier_ID FROM pathofinder_db.supplier
             WHERE supplier_name = "%s";""" %(supplier_name)
    supplier_tuple = execute_select_queries(sql)
    supplier_ID = supplier_tuple[0][0]
    return supplier_ID
    
    
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
        duplicated -- A boolean, False when oligo sequence is unique and True when duplicated"
    """
    # from import_oli_dict the info is obtained
    # and read into seq, fiveprime, threeprime and M1, M1pos
    
    # if sequence == sequence in db
    # raise some frame
    # choose whether commit and it will get a new batchnumber but not a new olinumber
    # or choose to abort
    sql = """SELECT sequence FROM pathofinder_db.oligo WHERE
            sequence = "%s" """ %(seq)
    seq_tuple = execute_select_queries(sql)
    # print seq_tuple
    # not unpacking tuple yet, just checking whether something is inside
    if seq_tuple:
        # when something is inside it means that the sequence is already inside database
        # then we need to check whether the labels are the same or not
        
        if check_labels_duplicated(seq, fiveprime, threeprime, M1, M1pos):
            duplicated = True
            print "sequence and labels duplicated"
        else:
            duplicated = False
            print "only sequence duplicated labels not"
    else:
        # when tuple is found empty, we can proceed importing the oligo
        duplicated = False
        print "sequence unique"

    print duplicated

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
        new_order_ID = new_order_no(table)    
    
    
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


if __name__ == "__main__":
##    new_batch_number("batch")
##    get_supplier_ID("IDT")
##    new_batch_number("batch")
    parse_importfile("Importfileoligos_new.csv")
##    check_sequence_duplicated("AATCACGAGGACCAAAGCACTGAATAACATTTTCCTCTCTGGTAGGGG") 
##    check_sequence_duplicated("AAT")
##    # these do not work yet as it finds 2 sequences
##    check_sequence_duplicated('TTTCCCTTCCTAACCTGGACATA', 'FAM', '', 'TAMRA', '23')
##    check_sequence_duplicated('TTTCCCTTCCTAACCTGGACATA', 'YY', 'BHQ1', 'TAMRA', '23')
##    check_sequence_duplicated('TTTCCCTTCCTAACCTGGACAT', 'FAM', '', 'TAMRA', '23')
##    check_sequence_duplicated('TTTCCCTTCCTAACCTGGACAT', 'YY', 'BHQ1', 'TAMRA', '23')
##    
