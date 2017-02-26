
"""
Author: Melanie van den Bosch
Script for exporting the order-out file after oligos
were imported to the PF database 
"""


import MySQLdb
import time
import datetime
import re
import config as cfg
from Table_update_queries import *
from Table_Lookup_queries import execute_select_queries
import csv


def get_from_db():
    """ Yields the rows from the db that were not ordered yet

    
    """
    # open connection
    db = MySQLdb.connect(cfg.mysql['host'], cfg.mysql['user'],
                         cfg.mysql['password'], cfg.mysql['database'])
    # prepare a cursor object
    cursor = db.cursor()
    # lookup and retrieve values
    # get a boolean here, that checks which oligos were selected for processing
    # if process = selected:
    sql = """SELECT * FROM pathofinder_db.order_out
                WHERE order_status = "processed";"""         
    db_rows_tuple = execute_select_queries(sql)
    for db_row in db_rows_tuple:
        yield db_row
        

def write_orderout():
    """ Returns a .csv file from the selected rows in the PF db

    Keyword arguments:
        db_rows: list of rows from the PF that have to be written
        to order-out file
    """
    with open("OrderOut.csv", "wb") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for db_row in get_from_db():
            writer.writerow(db_row)
            print db_row
##        order_out.write('oligo_ID,batch_number,oligo_name,sequence,'\
##'label5prime,label3prime,labelM1,labelM1position,synthesis_level_ordered,'\
##'purification_method,order_status,order_number,supplier_ID,supplier_name\n')
##        for db_row in get_from_db():
##            order_out.write("{0}\n".format(db_row))
##            print db_row
##            #for db_cell in db_row:
##                #order_out.write("{0}".format(db_cell))
            
            

if __name__ == "__main__":
    write_orderout()
