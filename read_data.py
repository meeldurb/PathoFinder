## Script to import the old db files into the new db
import config as cfg

def read_oligolist(filename):
    data = open(filename, 'r')
    for line in data:
        
        
        line = line.split(',')
        if "OLI" in line[0]:

            notes = line[47].split('|')
            print len(line)
            # OLIGO
            oligodict = {}
            
            oligodict[cfg.db_tables_views['oligo'][0]] = line[0]     # OLI ID
            oligodict[cfg.db_tables_views['oligo'][1]] = line[11]    # Oli name
            # newdict[cfg.db_tables_views['oligo'][2]] = line[0]     # Oli Type
            oligodict[cfg.db_tables_views['oligo'][3]] = line[12]    # Seq
            oligodict[cfg.db_tables_views['oligo'][4]] = line[15]    # description
            oligodict[cfg.db_tables_views['oligo'][5]] = line[6]     # Entry Date
            oligodict[cfg.db_tables_views['oligo'][6]] = line[8]     # Creator
            oligodict[cfg.db_tables_views['oligo'][7]] = line[7]     # Update Date
            oligodict[cfg.db_tables_views['oligo'][8]] = line[9]     # Modifier
            oligodict[cfg.db_tables_views['oligo'][9]] = line[23]    # label5
            oligodict[cfg.db_tables_views['oligo'][10]] = line[24]   # label3
            oligodict[cfg.db_tables_views['oligo'][11]] = line[25]   # labelM1
            oligodict[cfg.db_tables_views['oligo'][12]] = line[28]   # LabelM1Pos
            # newdict[cfg.db_tables_views['oligo'][13]] = line[0]    # pathogen
            # newdict[cfg.db_tables_views['oligo'][14]] = line[0]    # target
            # newdict[cfg.db_tables_views['oligo'][15]] = line[0]    # notes

            # BATCH
            batchdict = {}

  #          oligodict[cfg.db_tables_views['batch'][0]] = line[0]    # batch_number
#            oligodict[cfg.db_tables_views['batch'][1]] = line[0]    # OLI ID
 #           oligodict[cfg.db_tables_views['batch'][2]] = line[0]    # synth ord
   #         oligodict[cfg.db_tables_views['batch'][3]] = line[0]    # purify method
    #        oligodict[cfg.db_tables_views['batch'][4]] = line[0]    # synth del
     #       oligodict[cfg.db_tables_views['batch'][5]] = line[0]    # spec sheet
      #      oligodict[cfg.db_tables_views['batch'][6]] = line[0]    # order number
       #     oligodict[cfg.db_tables_views['batch'][7]] = line[0]    # del date
        #    oligodict[cfg.db_tables_views['batch'][8]] = line[0]    # order status










if __name__ == "__main__":
    filename  = "../PathoFinder db/2016-09-21 Oligolist PF.xlsx - Sheet1.csv"
    read_oligolist(filename)
    
    
