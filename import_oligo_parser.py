"""
Author: Melanie van den Bosch
Script for parsing import oligos into dictionary
Script "query_functies_as_dictionary.py" puts these inside
SQL database
"""

import csv
import query_functies_as_dictionary
import time
import datetime

def open_file(filename):
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
    import_dict = {}
    # read in the column names and make dictionary keys
    header = import_data.readline().strip()
    header_colnames = header.split(";")
    print header_colnames
    for name in header_colnames:
        import_dict[name] = ""
    print import_dict
    # Every row fills the values of the dict
    # at the end it is imported to the database and emptied
        for row in import_dict:
            
def get_date_stamp():
    """Returns a string of the current date in format DD-MM-YYYY"""
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    return date   
