
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

empty = True

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
    if db_rows_tuple:
        for db_row in db_rows_tuple:
            yield db_row
    else:
        print "No oligo's found with order_status 'processed'"

        

def write_orderout():
    """ Returns a .csv file from the selected rows in the PF db

    Keyword arguments:
        db_rows: list of rows from the PF that have to be written
        to order-out file
    """
    with open("OrderOut.csv", "wb") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        header = ('oligo_ID','batch_number','oligo_name','sequence',
                  'label5prime','label3prime','labelM1','labelM1position',
                  'synthesis_level_ordered','purification_method','order_status',
                  'order_number','supplier_ID','supplier_name')
        writer.writerow(header)
        for db_row in get_from_db():
            if db_row:
                writer.writerow(db_row)
            else:
                "No file was written"


def change_status():
    """ Changed status of oligos from processed to ordered

    Checks if order-out file was written and then changes order status
    """
    update_row("Batch", { "order_status":"processed"},
                   {"batch_number": "20170005", "order_status":"ordered"})
    #print "No oligo's found with order_status 'processed'"
            

if __name__ == "__main__":
    write_orderout()
    change_status()
    
    
