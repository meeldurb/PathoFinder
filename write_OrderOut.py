
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
    with open("OrderOut.csv", "w") as order_out:
        for db_row in get_from_db():
            order_out.write("\n")
            for db_cell in db_row:
                order_out.write(",{0},".format(db_cell))
            
            

if __name__ == "__main__":
    write_orderout()
