## Script to import the old db files into the new db
import config as cfg
import re
import Table_update_queries as TUQ
import Table_Lookup_queries as TLQ
import MySQLdb

def read_oligolist(filename, start_OLI_ID):
    """Import the data from a .tsv file into the database

    Keyword Arguments:
    filename        -- string, filepath to importfile. only .tsv extension!
    start_OLI_ID    -- string, the whole OLI ID of the row to start importing from"""
    data = open(filename, 'r')
    start = False
    for line in data:
        line = line.split('\t')
        
        # Start from the OLI ID from input
        if line[0] == start_OLI_ID:
            start = True
            
        if start == True:
            if "OLI" in line[0]:
                print line[0]        

                # OLIGO
                oligodict = {}
                
                # Retrieve employee_ID's for creator and modifier
                creator = TLQ.search_in_single_attribute('employee', 'emp_name', line[8])[0][0]
                modifier = TLQ.search_in_single_attribute('employee', 'emp_name', line[9])[0][0]

                # Create new dates
                entry_date = convertdate(line[6])
                mod_date = convertdate(line[7])
                

                
                oligodict[cfg.db_tables_views['oligo'][0]] = line[0]     # OLI ID
                oligodict[cfg.db_tables_views['oligo'][1]] = line[11]    # Oli name
                # newdict[cfg.db_tables_views['oligo'][2]] = line[0]     # Oli Type
                oligodict[cfg.db_tables_views['oligo'][3]] = line[12]    # Seq
                oligodict[cfg.db_tables_views['oligo'][4]] = line[15]    # description
                oligodict[cfg.db_tables_views['oligo'][5]] = entry_date    # Entry Date
                oligodict[cfg.db_tables_views['oligo'][6]] = creator     # Creator
                oligodict[cfg.db_tables_views['oligo'][7]] = mod_date     # Update Date
                oligodict[cfg.db_tables_views['oligo'][8]] = modifier    # Modifier
                oligodict[cfg.db_tables_views['oligo'][9]] = line[23]    # label5
                oligodict[cfg.db_tables_views['oligo'][10]] = line[24]   # label3
                oligodict[cfg.db_tables_views['oligo'][11]] = line[25]   # labelM1
                oligodict[cfg.db_tables_views['oligo'][12]] = line[28]   # LabelM1Pos
                # newdict[cfg.db_tables_views['oligo'][13]] = line[0]    # pathogen
                # newdict[cfg.db_tables_views['oligo'][14]] = line[0]    # target
                # newdict[cfg.db_tables_views['oligo'][15]] = line[0]    # notes

                # Insert into Oligo
                try:
                    TUQ.insert_row('oligo', oligodict)
                except MySQLdb.Error,e:
                    raise ValueError(e[0], e[1])
                
                # BATCH
                batchdict = {}

                # split up notes to retrieve batchnumbers
                notes = line[47].split('|')

                # only continue if notes contain something
                if len(notes) > 1:
                
                    # Retrieve batchnumber
                    batch_pattern = re.compile(r'OligoBatchNr ([0-9]*)')
                    batch_match = batch_pattern.search(notes[1])
                    batch_nr = batch_match.group(1)
                    # Retrieve Application number
                    app_pattern = re.compile(r'Application ([0-9]*)')
                    app_match = app_pattern.search(notes[2])
                    app_nr = app_match.group(1)

                    if batch_nr != None:
                        batchdict[cfg.db_tables_views['batch'][0]] = batch_nr     # batch_number
                        batchdict[cfg.db_tables_views['batch'][1]] = line[0]            # OLI ID

                        #synthesis level does not always have a value
                        if line[19] == '':
                            line[19] = '00000'
                        batchdict[cfg.db_tables_views['batch'][2]] = line[19]    # synth ord
                        
               #         batchdict[cfg.db_tables_views['batch'][3]] = line[0]    # purify method
                #        batchdict[cfg.db_tables_views['batch'][4]] = line[0]    # synth del
                 #       batchdict[cfg.db_tables_views['batch'][5]] = line[0]    # spec sheet
                  #      batchdict[cfg.db_tables_views['batch'][6]] = line[0]    # order number
                   #     batchdict[cfg.db_tables_views['batch'][7]] = line[0]    # del date
                        batchdict[cfg.db_tables_views['batch'][8]] = "Delivered"    # order status


                        # Insert into Batch
                        try:
                            TUQ.insert_row('batch', batchdict)
                        except MySQLdb.Error,e:
                            raise ValueError(e[0], e[1])

def convertdate(datetimestamp):
    """Converts a String date : 22-05-2011 to 22/05/2011"""

    pattern = re.compile(r'([0-9]+-[0-9]+-[0-9]+) ')
    match = pattern.search(datetimestamp)
    match = match.group(1)
    result = re.sub(r'-','/', match)
    return result
    
if __name__ == "__main__":
    filename  = "../PathoFinder db/2016-09-21 Oligolist PF.xlsx - Sheet1.tsv"
    read_oligolist(filename, 'OLI000003')
    
    
