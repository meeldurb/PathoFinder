"""
Author: Melanie van den Bosch
Jorn van der Ent
Script for having multiple windows frames in a GUI
and functionality
"""


## When you want to add a page, simply create a new class
## put the page its classname inside the Frames for-loop
## and add the page in the Startpage class under commands
from __future__ import division
import math
import sys
import os
import Tkinter as tk
import tkFont
from tkFileDialog import askopenfilename
import MySQLdb
import config as cfg
import Table_Lookup_queries as TLQ
import table_windows as tw
import Table_update_queries as TUQ
#from import_oligo_parser import new_emp_ID
#from import_oligo_parser import get_date_stamp
#from import_oligo_parser import import_to_queue
#from import_oligo_parser import make_new_ID
import import_oligo_parser as IOP



mycolor = '#%02x%02x%02x' % (0, 182, 195)
LARGE_FONT = ("Corbel", 20)
LARGE_FONT = ("Corbel", 18)
LARGE_FONT = ("Corbel", 14)



class OligoDatabase(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # setting a default font for complete GUI
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Corbel", size=20)
        self.tk_setPalette(background=mycolor, foreground="white",
                           activeBackground="grey", activeForeground="black")
        
        container = tk.Frame(self, width=300, height=200)

        # the container is where a bunch of frames will be stacked on top
        # of eachother, then the one we want visible will be raised
        # above the others
        container.pack(side="top", fill="both", expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Make a dictionary with variables which can be accessed from all the classes
        self.shared_data = {
            "username" : tk.StringVar(),
            'password' : tk.StringVar(),
            "table" : tk.StringVar(),
            "search" : tk.StringVar()
            }

        for F in (Login, Home, TableViews, OrderStatus, Import, Experiment, ChangePassword,
                  Experiment, SearchPage, Admin, Employees, AddEmployee, OrderBin, BinToQueue,
                  QueueToBin, ProcessQueue,
                  OrderStatus, OrderQueue, Deliveries, OutOfStock, GeneralOrderStatus, RemoveUser,
                  AdminRights, AddSupplier, AddProject, RemoveOligo, Project, ModifyProject, Supplier,
                  ModifySupplier):
            page_name = F.__name__
            # the classes (.. Page) require a widget that will be parent of
            # the class and object that will serve as a controller
            # it creates an instance of the class (subclass of Frame widget),
            # and assigns it (temporarily) in frame
            frame = F(container, self)#parent=container, controller=self
            # passing self as second controller parameter, the new class
            # instances will be able to call methods in the OligoDB class object
            # key to dict is the page name
            self.frames[page_name] = frame

            # put all the pages in the same location;
            # the one on the top of the stacking order is the one visible
            frame.grid(row=0, column=0,  sticky="NSEW")

        self.title("PathoFinder Oligo DB")
        self.show_frame("Login")

    def show_frame(self, page_name):
        """ Raises the frame of the given page name to the top
        """
        frame = self.frames[page_name]
        frame.tkraise()
        
#############################________________LOGIN________________#############################

class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Corbel", size=24)
        self.tk_setPalette(background=mycolor, foreground="white",
                           activeBackground="grey", activeForeground="black")

        self.controller = controller
        self.password = tk.StringVar()
        self.var_message = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        label = tk.Label(self, text="Login")
        label.pack(side = 'top', pady = 20)

        # username
        groupuser = tk.LabelFrame(self, relief = 'flat')
        groupuser.pack(side = 'top')      
        
        user_label = tk.Label(groupuser, text = "Username: ", width = 10)
        user_label.pack(side = 'left', padx = 10, pady = 5)
        
        user = tk.Entry(groupuser)
        user['textvariable'] = self.username
        user.pack(side = 'right', padx = 10, pady = 5)

        # password
        grouppass = tk.LabelFrame(self, relief = 'flat')
        grouppass.pack(side = 'top')
        
        pw_label = tk.Label(grouppass, text = "Password: ", width = 10)
        pw_label.pack(side = 'left', padx = 10, pady = 5)
                  
        pw = tk.Entry(grouppass, show = "*")
        pw['textvariable'] = self.password
        pw.pack(side = 'right', padx = 10, pady = 5)

        # Button
        login_button = tk.Button(self, text = "Login")
        login_button['command'] = lambda: self.check_login()
        login_button.pack(side = 'top', padx = 10, pady = 5)

        # Message
        msg = tk.Message(self, width=280)
        msg['textvariable'] = self.var_message
        msg.pack(side = 'top', pady = 5)

    def check_login(self):
        """Check whether Login details are valid, in order to continute"""
        self.controller.shared_data["username"].set(self.username.get())
        self.controller.shared_data["password"].set(self.password.get())
        try:
            db = MySQLdb.connect(cfg.mysql['host'], self.controller.shared_data["username"].get(), self.controller.shared_data["password"].get(), cfg.mysql['database'])
            db.close()
            self.controller.show_frame("Home")
        except:
            self.var_message.set("Invalid username or password")
        # Empty the entry fields
        self.username.set("")
        self.password.set("")

#############################________________HOME________________#############################
          
class Home(tk.Frame):
    def __init__(self, parent, controller):
        # each page is a subblass of tk.Frame class, this calls
        # constructor of parent class
        # necessary to initialize internal structures that make up frame widget
        # send in a ref to another widget which is to act as the parent
        # of this new widget
        tk.Frame.__init__(self, parent)


        #save a reference to controller in each page:
        self.controller = controller
        

        label = tk.Label(self, text = "Home")
        label.pack(side = 'top', pady = 20 )

        # Main ButtonsGroup
        groupmain = tk.LabelFrame(self, relief = 'flat')
        groupmain.pack(side = 'top')

        # Group for Buttons CentreLeft
        groupleft = tk.LabelFrame(groupmain, relief = 'flat')
        groupleft.pack(side = 'left', pady = 5, padx= 10)
        
        button1 = tk.Button(groupleft, text="Import oligos", width = 15,
                            command=lambda:controller.show_frame("Import"))
        button1.pack(side = 'top', pady = 5, padx = 10)

        button2 = tk.Button(groupleft, text="Views", width = 15,
                         command=lambda:controller.show_frame("TableViews"))
        button2.pack(side = 'top', pady = 5, padx = 10)

##        button3 = tk.Button(groupleft, text="Experiment", width = 15,
##                        command=lambda:controller.show_frame("Experiment"))
##        button3.pack(side = 'top', pady = 5, padx = 10)
        
        # Group for Buttons CentreRight
        groupright = tk.LabelFrame(groupmain, relief = 'flat')
        groupright.pack(side = 'right', pady = 5, padx= 10)
        
        button4 = tk.Button(groupright, text="Order-Status", width = 15,
                        command=lambda:controller.show_frame("OrderStatus"))
        button4.pack(side = 'top', pady = 5, padx = 10)

        button5 = tk.Button(groupright, text="Search", width = 15,
                        command=lambda:controller.show_frame("SearchPage"))
        button5.pack(side = 'top', pady = 5, padx = 10)

        # Group for AdminButtons
        groupmainad = tk.LabelFrame(self, relief = 'flat')
        groupmainad.pack(side = 'top', pady = 30)
        
        button6 = tk.Button(groupmainad, text="Change password", width = 15,
                        command=lambda:controller.show_frame("ChangePassword"))
        button6.pack(side = 'top', pady = 5, padx = 10)

        button7 = tk.Button(groupmainad, text = "Admin", width = 15,
                            command = lambda : self.popup_password())
        button7.pack(side = 'top', pady = 5, padx = 10)

        # Group for Log Buttons
        grouplog = tk.LabelFrame(self, relief = 'flat')
        grouplog.pack(side = 'bottom')        

        button8 = tk.Button(grouplog, text="Log off & Quit",  width = 15,
                            command = controller.destroy)
        button8.pack(side = 'left', pady = 5, padx = 10)

        button9 = tk.Button(grouplog, text="Log off",  width = 15,
                            command=lambda : controller.show_frame("Login"))
        button9.pack(side = 'right', pady = 5, padx = 10)

    def popup_password(self):
        self.win = tk.Toplevel()

        self.password = tk.StringVar()
        self.var_message = tk.StringVar()

        label = tk.Label(self.win, text = 'Enter password :')
        label.pack(side = 'top')

        entry = tk.Entry(self.win, textvariable = self.password, show = "*")
        entry.pack(side = 'top')

        msg = tk.Message(self.win, textvariable = self.var_message, width = 280)
        msg.pack(side = 'top')
        
        button1 = tk.Button(self.win, text = 'OK',
                            command = lambda : self.check_admin())
        button1.pack(side = 'top')

    def check_admin(self):
        if self.password.get() != self.controller.shared_data["password"].get():
            self.var_message.set("You are not the current user, please Login using your own credentials")
        else: 
            sql = "SHOW GRANTS FOR %s@%s" % (self.controller.shared_data["username"].get(), cfg.mysql['hostadress'])
            # Try to open connection, won't work if password is incorrect
            try:
                db = MySQLdb.connect(cfg.mysql['host'], self.controller.shared_data["username"].get(), self.controller.shared_data["password"].get(), cfg.mysql['database'])
            except:
                self.var_message.set("Incorrect Password")

            if self.var_message.get() != "Incorrect Password": # so connection succesfully established

                cursor = db.cursor()
                try:
                    cursor.execute(sql)
                    match = cursor.fetchall()
                except MySQLdb.Error,e:
                    print e[0], e[1]
                    db.rollback()
                cursor.close()
                db.close()
                if match != None:
                    admin = False   # initialize
                    for elem in match:     # could be more than one returns in the tuple!
                        if "WITH GRANT OPTION" in elem[0]:
                            admin = True

                    # Execute when admin is true, otherwise give error
                    if admin == True:
                        self.win.destroy()
                        self.controller.show_frame('Admin')
                    else:
                        self.var_message.set("You are not authorized")
                else:
                    self.var_message.set("You are not authorized")

#############################________________VIEWS________________#############################

class TableViews(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="Table Views")
        label.grid(columnspan=8, pady=10)



        button2 = tk.Button(self, text="Oligos with most recent Batches",
                        command = lambda : TLQ.build_query_and_table("oligo_recent_batch"))
                            
        button2.grid(row=2, column=1, pady=5, padx=10, sticky="WE")

        button3 = tk.Button(self, text="Batch, Order & Supplier",
                        command=lambda:TLQ.build_query_and_table("batches_order_supplier"))
                          
        button3.grid(row=3, column=1, pady=5, padx=10, sticky="WE")

        button4 = tk.Button(self, text="Supplier analytics",
                        command=lambda: TLQ.build_query_and_table('suppliers_analysis'))
                        
        button4.grid(row=4, column=1, pady=5, padx=10, sticky="EW")

        button5 = tk.Button(self, text="Projects",
                        command=lambda:TLQ.build_query_and_table("oligos_from_project"))

        button5.grid(row=5, column=1, pady=5, padx=10, sticky="EW")

        button6 = tk.Button(self, text="Everything",
                        command=lambda:TLQ.build_query_and_table("everything"))

        button6.grid(row=6, column=1, pady=5, padx=10, sticky="EW")

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
                            
        button1.grid(row=7, column=3, pady=5, padx=10)


#############################________________IMPORT________________#############################

class Import(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.path_var = tk.StringVar()
        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="Entry of New Oligos")
        label.grid(row=1, columnspan=8, pady=10)

        button2 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button2.grid(row=10, column=9, pady=5, padx=10, sticky="EW")

     
        label2 = tk.Label(self, text="Import from file at location:")
        label2.grid(row=8, column=1, pady=5, padx=10)

        text_path = tk.Entry(self, bg='white', fg='black', width=50,
                             textvariable=self.path_var, justify="left" )
                                # add feature that it will expand upon selection
                                # add that when upload was succesfull, path dissappears
        text_path.grid(row=8, column=3, columnspan=4)

        button3 = tk.Button(self, text="Browse",
                            command=lambda:self.path_var.set(askopenfilename()))
        button3.grid(row=8, column=7)

        button4 = tk.Button(self, text="Upload",
                            command=lambda:IOP.import_to_queue("order_queue",
                                                           self.path_var.get()))
                            #command = Uploads the file in the path into the
                            # specified columns of the db
        button4.grid(row=8, column=8)

class Experiment(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        
        label = tk.Label(self, text="Experiments")
        label.grid(columnspan=8, pady=10)

        button2 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button2.grid(row=10, column=9, pady=5, padx=10, sticky="EW")


class ChangePassword(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        self.cpassword = tk.StringVar()
        self.npassword = tk.StringVar()
        self.rnpassword = tk.StringVar()
        self.var_message = tk.StringVar()
        
        label = tk.Label(self, text="Change Password")
        label.grid(row = 1, column = 1, columnspan=8, pady=10)

        # currrent password
        cpwlabel = tk.Label(self, text = "Current Password: ")
        cpwlabel.grid(row = 3, column = 2, pady=10)

        cpw = tk.Entry(self, show = "*")
        cpw['textvariable'] = self.cpassword
        cpw.grid(row = 3, column = 4, columnspan = 4, pady = 10)

        # new password
        npwlabel = tk.Label(self, text = "New Password: ")
        npwlabel.grid(row = 4, column = 2, pady=10)

        npw = tk.Entry(self, show = "*")
        npw['textvariable'] = self.npassword
        npw.grid(row = 4, column = 4, columnspan = 4, pady = 10)

        # repeat password
        rnlabel = tk.Label(self, text = "Repeat New Password: ")
        rnlabel.grid(row = 5, column = 2, pady=10)

        rnpw = tk.Entry(self, show = "*")
        rnpw['textvariable'] = self.rnpassword
        rnpw.grid(row = 5, column = 4, columnspan = 4, pady = 10)

        # Message
        msg = tk.Message(self, width=280)
        msg['textvariable'] = self.var_message
        msg.grid(row=6, column=2, columnspan=4, pady = 10)

        # Button
        changpass = tk.Button(self, text = "Confirm")
        changpass['command'] = lambda: self.change_password()
        changpass.grid(row = 7, column = 4, pady = 10)


        button2 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button2.grid(row=9, column=9, pady=5, padx=10, sticky="EW")

    def change_password(self):
        """Change Password for current user"""
        
        # check new and repeat new are equel
       
        if self.npassword.get() != self.rnpassword.get():
            self.var_message.set("New passwords are not entered correctly")
        else:
            # check whether entered current password is correct       
            try:
                db = MySQLdb.connect(cfg.mysql['host'], self.controller.shared_data["username"].get(),
                                     self.controller.shared_data["password"].get(),
                                     cfg.mysql['database']) # open connection
            except:
                self.var_message.set("Current Password not correct")
            if self.var_message.get() != "Current Password not correct":

                cursor = db.cursor()

                # Retrieve query to alter employee table
                update_table_sql = TUQ.make_update_row('Employee', { 'password' : self.npassword.get()},
                                                       {'emp_name' : self.controller.shared_data["username"].get()})

                # Make a sql to change password
                alter_pass_sql = "ALTER USER %s@%s IDENTIFIED BY '%s';" % (self.controller.shared_data["username"].get(),
                                                                           cfg.mysql['hostadress'], self.npassword.get())

                # Execute
                try:
                    cursor.execute(update_table_sql)
                    cursor.execute(alter_pass_sql)
                    db.commit()
                    cursor.close()
                    db.close()
                    self.controller.shared_data["password"].set(self.npassword.get()) # Set new password into the programm
                    self.var_message.set("Password Changed Succesfully")
                except MySQLdb.Error,e:# Rollback in case there is any error
                    db.rollback()
                    raise ValueError(e[0], e[1])
                    cursor.close()
                    db.close() #disconnect from server
        # Empty the Entry fields
        self.cpassword.set("")
        self.npassword.set("")
        self.rnpassword.set("")

#############################________________SEARCH________________#############################

# Stand-alone search window
class SearchPage(tk.Frame):
    # call using: SearchPage(tk.Tk(), "table")
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        # set variables

        self.controller = controller

        self.frame = parent
        self.tables = cfg.db_tables_views.keys()
        # Remove Employee table from the options
        del self.tables[self.tables.index('employee')]

        self.table = tk.StringVar()
        self.table.set(self.tables[0])
        self.search_input = tk.StringVar()

        # initialize check for the presence of the subFrame
        self.restsearchpresence = tk.BooleanVar()
        self.restsearchpresence.set(False)

        # Search Group
        search_group = tk.LabelFrame(self, relief = 'flat')
        search_group.pack(side = 'top', padx=10, pady=10)
        
        search_label = tk.Label(search_group, text = 'Search for: ')
        search_label.pack(side = 'left', padx=10, pady=10)

        search_entry = tk.Entry(search_group, width = 50)
        search_entry['textvariable'] = self.search_input
        search_entry.pack(side = 'left', padx=10, pady=10)

        # tablemenu group
        tablelabel =tk.Label(self, text = 'Choose table to search in:')
        tablelabel.pack(side = 'top', padx=10, pady=10)
        
        tablesmenu = tk.OptionMenu(self, self.table, *self.tables)
        tablesmenu.pack(side = 'top', padx = 10, pady = 10)

        buttonsgroup = tk.LabelFrame(self, relief = 'flat')
        buttonsgroup.pack(side = 'top', padx = 10, pady = 10)
        
        # Cancel
        cancelbutton = tk.Button(buttonsgroup, text = 'Back to Home')
        cancelbutton['command'] = lambda: self.cancelbutton()
        cancelbutton.pack(side = 'right', padx = 5, pady = 10)
        
        # Continue to open the other options
        continuebutton = tk.Button(buttonsgroup, text = "Continue")
        continuebutton["command"] = lambda : self.searchrestadd()
        continuebutton.pack(side = 'right', padx = 5, pady = 10)

    def cancelbutton(self):
        # if subFrame is present, destroy
        if self.restsearchpresence.get():
            self.restframe.destroy()
        self.controller.show_frame("Home")

    def searchrestadd(self):
        if self.restsearchpresence.get():
            self.restframe.destroy()
        # Feed the data to the Gui variables:
        self.controller.shared_data["table"].set(self.table.get())
        self.controller.shared_data["search"].set(self.search_input.get())

        # Set the presence to True, and add subFrame to the current Frame
        self.restsearchpresence.set(True)
        self.restframe = SearchRest(self.controller)
        self.restframe.pack(in_ = self, side = 'bottom')

class SearchRest(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self)

        self.controller = controller

        self.table = self.controller.shared_data["table"].get()
        self.search_input = self.controller.shared_data["search"].get()

        self.sortattribute = tk.StringVar()
        self.sortattribute.set(cfg.db_tables_views[self.table][0])
        self.sortmethod = tk.StringVar()
        self.sortmethod.set("Descending")
        
        # Sort Group
        sort_group = tk.LabelFrame(self, text = 'Sort By', relief = 'flat')
        sort_group.pack(side = 'top', padx=10, pady = 10)
        
        sortList = tk.OptionMenu(sort_group, self.sortattribute, *cfg.db_tables_views[self.table])
        sortList.pack(side='left', padx=5, pady=5)

        sortmethodList = tk.OptionMenu(sort_group, self.sortmethod, 'Ascending', 'Descending')
        sortmethodList.pack(side='left', padx=5, pady=5)


        # Go
        sortbutton = tk.Button(self, text = 'GO', padx = 20, pady = 10)
        sortbutton['command'] = lambda : self.search_button_go(self.table, self.search_input, self.sortattribute.get(), self.sortmethod.get())
        # To clarify: for some weird reason self.search_input.get()didn't work, so had to use search_entry.get() instead.
        sortbutton.pack(side = 'bottom' , padx=5, pady=10)

    def search_button_go(self, table_str, search_input, sortattribute, sortmethod):
        sql, attributes = TLQ.search(table_str, search_input, sortattribute, sortmethod)
        self.destroy()
        TLQ.build_table_window(sql, table_str, attributes, sortattribute, sortmethod)
        
#############################________________ADMIN________________#############################

class Admin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="Admin")
        label.pack(side = 'top', pady=10)

        groupmain = tk.LabelFrame(self, relief = 'flat')
        groupmain.pack(side = 'top', pady = 5, padx= 10)
        
        groupleft = tk.LabelFrame(groupmain, relief = 'flat')
        groupleft.pack(side = 'left', pady = 5, padx= 10)
        
        button1 = tk.Button(groupleft, text="Order Bin", width = 15,
                            command = lambda : self.controller.show_frame("OrderBin"))
        button1.pack(side = 'top', pady=5, padx=10)

        button2 = tk.Button(groupleft, text="Employees", width = 15,
                         command = lambda : self.controller.show_frame("Employees"))
        button2.pack(side = 'top', pady=5, padx=10)

        button3 = tk.Button(groupleft, text="Order Status", width = 15,
                         command = lambda : self.controller.show_frame("GeneralOrderStatus"))
        button3.pack(side = 'top', pady=5, padx=10)

        groupright = tk.LabelFrame(groupmain, relief = 'flat')
        groupright.pack(side = 'right', pady = 5, padx= 10)
        
        button5 = tk.Button(groupright, text = 'Remove Oligo', width = 15,
                            command = lambda : self.controller.show_frame("RemoveOligo"))
        button5.pack(side = 'top', pady = 5, padx= 10)

        button6 = tk.Button(groupright, text = "Projects", width = 15,
                            command = lambda : self.controller.show_frame("Project"))
        button6.pack(side = 'top', pady = 5, padx = 10)
        
        button6 = tk.Button(groupright, text = "Suppliers", width = 15,
                            command = lambda : self.controller.show_frame("Supplier"))
        button6.pack(side = 'top', pady = 5, padx = 10)


        groupnav = tk.LabelFrame(self, relief = 'flat')
        groupnav.pack(side = 'bottom', pady = 5, padx= 10)
        
        button4 = tk.Button(groupnav, text="Back to Home",
                         command=lambda:self.controller.show_frame("Home"))
                            
        button4.pack(side = 'left', pady=5, padx=10)

class RemoveOligo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        self.oligo = tk.StringVar()
        self.var_message = tk.StringVar()
        
        label = tk.Label(self, text="Remove Oligo")
        label.pack(side = 'top', pady=10)

        group2 = tk.LabelFrame(self, relief = 'flat')
        group2.pack(side = 'top', pady = 5, padx = 10)
        
        labeloli = tk.Label(group2, text = 'Oligo ID: ')
        labeloli.pack(side = 'left', pady=10)

        oligo = tk.Entry(group2)
        oligo['textvariable'] = self.oligo
        oligo.pack(side = 'left', pady = 10)

        # Message
        msg = tk.Message(self, width=500)
        msg['textvariable'] = self.var_message
        msg.pack(side = 'top', pady = 10)

        # Button
        confirm = tk.Button(self, text = "Remove")
        confirm['command'] = lambda: self.popup()
        confirm.pack(side = 'top', pady = 10)

        group3 = tk.LabelFrame(self, relief = 'flat')
        group3.pack(side = 'top', pady = 5, padx = 10)
        
        button2 = tk.Button(group3, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button2.pack(side = 'left', pady=5, padx=10)

        button3 = tk.Button(group3, text="Back to Admin",
                         command=lambda:controller.show_frame("Admin"))
        button3.pack(side = 'right', pady=5, padx=10)


    def popup(self):
        """ A popup window which asks to confirm action"""
        self.win = tk.Toplevel()

        label0 = tk.Label(self.win, text = ("Are you sure you want to remove '%s' ?" % self.oligo.get()))
        label0.pack(side = 'top', pady = 5)

        buttongroup = tk.LabelFrame(self.win, relief = 'flat')
        buttongroup.pack(side = 'top')
      
        button1 = tk.Button(buttongroup, text = 'Confirm',
                            command = lambda : self.remove())
        button1.pack(side = 'left', padx = 5, pady = 10)

        button2 = tk.Button(buttongroup, text = 'Cancel',
                            command = lambda : self.win.destroy())
        button2.pack(side = 'left', padx = 5, pady = 10)

    def remove(self):
        """Remove an oligo completely from the database when it has not yet been delivered"""

        # destroy popup window
        self.win.destroy()
        
        # Get oligo_ID name, check whether not empty
        oligo_ID = self.oligo.get()
        oligo_ID = oligo_ID.strip()
        if oligo_ID == "":
                self.var_message.set("Invalid oligo_ID")
        else:
            db = MySQLdb.connect(cfg.mysql['host'], self.controller.shared_data["username"].get(),
                                 self.controller.shared_data["password"].get(), cfg.mysql['database']) # open connection
            cursor = db.cursor() # prepare a cursor object

            # Check whether ordered before (number of batches), if not; get batchnumber and orderstatus and ordernumber
            batch_sql = "SELECT batch_number, order_status, order_number FROM `batch` \
                            WHERE `batch`.oligo_ID = '%s'" % oligo_ID            
            try:
                cursor.execute(batch_sql)
                batches = cursor.fetchall()
            except MySQLdb.Error,e:
                cursor.close()
                db.close()
                self.var_message.set((e[0], e[1]))

            # Continue if it is the only batch
            if len(batches) == 1:
                batch = batches[0]
                # check whether orderstatus is not in deleiverd or out of stoc
                if batch[1] != 'Delivered' and batch[1] != 'Out of Stock':
                    # Check number of batches in ordernumber
                    no_of_batches_order_sql = "SELECT COUNT(batch_number) FROM `batch` WHERE `batch`.order_number =  '%s'" % batch[2] 

                    # Make a sql for removal of oligo from oligo table
                    del_from_oli = TUQ.make_delete_row('oligo', {'oligo_ID' : oligo_ID})

                    # Make a sql for removal of batch from batch table
                    del_from_batch = TUQ.make_delete_row('batch', {'batch_number' : batch[0]})

                    # Make a sql for removal from project.oligo table
                    del_from_oliproj = TUQ.make_delete_row('project_oligo', {'oligo_ID' : oligo_ID})
            
                    # Find the number of batches in the ordernumber, already remove oligo from batch and olig
                    try:
                        cursor.execute(no_of_batches_order_sql)
                        count = cursor.fetchall()
                        cursor.execute(del_from_batch)
                        cursor.execute(del_from_oliproj)
                        cursor.execute(del_from_oli)
                        db.commit()
                        self.var_message.set("Oligo %s Removed" % oligo_ID)
                    except MySQLdb.Error,e:
                        db.rollback()
                        cursor.close()
                        db.close()
                        self.var_message.set((e[0], e[1]))

                    # Continue when count equals to one
                    if count[0][0] == 1:
                        # Make a sql for removal of batch from batch table
                        del_from_order = TUQ.make_delete_row('order', {'order_number' : batch[2]})
                    
                        # Remove order as well
                        try:
                            cursor.execute(del_from_order)
                            db.commit()
                            self.var_message.set("Oligo %s & Order %s Removed" % (oligo_ID, batch[2]))
                        except MySQLdb.Error,e:
                            db.rollback()
                            cursor.close()
                            db.close()
                            self.var_message.set((e[0], e[1]))
                # Don't remove when orderstatus is not in Ordererd or earlier
                else:
                    self.var_message.set("Order Status has advanced too far")
            # Don't remove when multiple batchnumbers of the oligo
            else:
                self.var_message.set("This oligo has been ordered before")
        self.oligo.set("")

        
#############################________________PROJECTS________________#############################
        
class Project(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        
        label = tk.Label(self, text="Projects")
        label.pack(side = 'top', pady=20)

        group1 = tk.LabelFrame(self, relief = 'flat')
        group1.pack(side = 'top', padx = 10, pady = 5)
        
        button1 = tk.Button(group1, text = 'View Projects', width = 15,
                            command = lambda : TLQ.build_query_and_table("project"))
        button1.pack(side = 'top', pady = 5, padx = 10)
        
        button2 = tk.Button(group1, text = 'Add Project', width = 15,
                            command = lambda : self.controller.show_frame("AddProject"))
        button2.pack(side = 'top', pady = 5, padx = 10)

        button3 = tk.Button(group1, text = 'Modify Project', width = 15,
                            command = lambda : self.controller.show_frame("ModifyProject"))
        button3.pack(side = 'top', pady = 5, padx = 10)

        group2 = tk.LabelFrame(self, relief = 'flat')
        group2.pack(side = 'bottom', pady = 5, padx = 10)
        
        button4 = tk.Button(group2, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button4.pack(side = 'left', pady=5, padx=10)

        button5 = tk.Button(group2, text="Back to Admin",
                         command=lambda:controller.show_frame("Admin"))
        button5.pack(side = 'right', pady=5, padx=10)


        
class AddProject(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        self.project = tk.StringVar()
        self.var_message = tk.StringVar()
        
        label = tk.Label(self, text="Add Project")
        label.pack(side = 'top', pady=10)

        group2 = tk.LabelFrame(self, relief = 'flat')
        group2.pack(side = 'top', pady = 5, padx = 10)
        
        labelproj = tk.Label(group2, text = 'Project Name: ')
        labelproj.pack(side = 'left', pady=10)

        project = tk.Entry(group2)
        project['textvariable'] = self.project
        project.pack(side = 'left', pady = 10)

        # Message
        msg = tk.Message(self, width=500)
        msg['textvariable'] = self.var_message
        msg.pack(side = 'top', pady = 10)

        # Button
        confirm = tk.Button(self, text = "Add")
        confirm['command'] = lambda: self.popup()
        confirm.pack(side = 'top', pady = 10)

        group3 = tk.LabelFrame(self, relief = 'flat')
        group3.pack(side = 'top', pady = 5, padx = 10)
        
        button2 = tk.Button(group3, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button2.pack(side = 'left', pady=5, padx=10)

        button3 = tk.Button(group3, text="Back to Projects",
                         command=lambda:controller.show_frame("Project"))
        button3.pack(side = 'right', pady=5, padx=10)


    def popup(self):
        """ A popup window which asks to confirm action"""
        self.win = tk.Toplevel()

        label0 = tk.Label(self.win, text = ("Are you sure you want to add '%s' ?" % self.project.get()))
        label0.pack(side = 'top', pady = 5)

        buttongroup = tk.LabelFrame(self.win, relief = 'flat')
        buttongroup.pack(side = 'top')
      
        button1 = tk.Button(buttongroup, text = 'Confirm',
                            command = lambda : self.add())
        button1.pack(side = 'left', padx = 5, pady = 10)

        button2 = tk.Button(buttongroup, text = 'Cancel',
                            command = lambda : self.win.destroy())
        button2.pack(side = 'left', padx = 5, pady = 10)

    def add(self):
        """Add a project to project-table """

        # Get project name, check whether not empty
        projectname = self.project.get()
        projectname = projectname.strip()
        if projectname == "":
                self.var_message.set("Invalid name")
        else:
            db = MySQLdb.connect(cfg.mysql['host'], self.controller.shared_data["username"].get(),
                                 self.controller.shared_data["password"].get(), cfg.mysql['database']) # open connection
            cursor = db.cursor() # prepare a cursor object

            # Make a sql for creation of new user
            add_project_sql = TUQ.make_insert_row('project', {'project_ID' : IOP.make_new_ID('project'), 'project_name' : self.project.get()})

            try:
                cursor.execute(add_project_sql)
                db.commit()
                cursor.close()
                db.close()
                self.var_message.set("%s Added" % self.project.get())
                self.win.destroy()
                
            except MySQLdb.Error,e:# Rollback in case there is any error
                db.rollback()
                cursor.close()
                db.close()
                self.var_message.set((e[0], e[1]))
        # Empty entry field
        self.project.set("")

        
class ModifyProject(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        self.oldname = tk.StringVar()
        self.newname = tk.StringVar()
        self.var_message = tk.StringVar()
        
        label = tk.Label(self, text="Modify Project")
        label.pack(side = 'top', pady=10)

        group2 = tk.LabelFrame(self, relief = 'flat')
        group2.pack(side = 'top', pady = 5, padx = 10)
        
        labelold = tk.Label(group2, text = 'Current Name: ')
        labelold.pack(side = 'left', pady=10)

        old = tk.Entry(group2)
        old['textvariable'] = self.oldname
        old.pack(side = 'left', pady = 10)
        
        group1 = tk.LabelFrame(self, relief = 'flat')
        group1.pack(side = 'top', pady = 5, padx = 10)
        
        labelnew = tk.Label(group1, text = 'New Name: ')
        labelnew.pack(side = 'left', pady=10)

        new = tk.Entry(group1)
        new['textvariable'] = self.newname
        new.pack(side = 'left', pady = 10)
        
        # Message
        msg = tk.Message(self, width=500)
        msg['textvariable'] = self.var_message
        msg.pack(side = 'top', pady = 10)

        # Button
        confirm = tk.Button(self, text = "Confirm")
        confirm['command'] = lambda: self.change()
        confirm.pack(side = 'top', pady = 10)

        group3 = tk.LabelFrame(self, relief = 'flat')
        group3.pack(side = 'top', pady = 5, padx = 10)
        
        button2 = tk.Button(group3, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button2.pack(side = 'left', pady=5, padx=10)

        button3 = tk.Button(group3, text="Back to Projects",
                         command=lambda:controller.show_frame("Project"))
        button3.pack(side = 'right', pady=5, padx=10)

    def change(self):
        try:
            TUQ.update_row('project', {'project_name' : self.newname.get()}, {'project_ID' : self.oldname.get()})
            self.var_message.set("Name of %s Updated to %s" % (self.oldname.get(), self.newname.get()))
            # Empty the entry fields
            self.oldname.set("")
            self.newname.set("")
        except:
            self.var_message.set("An Error occured during processing, not executed")
            
#############################________________SUPPLIERS________________#############################

class Supplier(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        
        label = tk.Label(self, text="Supplieres")
        label.pack(side = 'top', pady=20)

        group1 = tk.LabelFrame(self, relief = 'flat')
        group1.pack(side = 'top', padx = 10, pady = 5)
        
        button1 = tk.Button(group1, text = 'View Suppliers', width = 15,
                            command = lambda : TLQ.build_query_and_table("supplier"))
        button1.pack(side = 'top', pady = 5, padx = 10)
        
        button2 = tk.Button(group1, text = 'Add Supplier', width = 15,
                            command = lambda : self.controller.show_frame("AddSupplier"))
        button2.pack(side = 'top', pady = 5, padx = 10)

        button3 = tk.Button(group1, text = 'Modify Supplier', width = 15,
                            command = lambda : self.controller.show_frame("ModifySupplier"))
        button3.pack(side = 'top', pady = 5, padx = 10)

        group2 = tk.LabelFrame(self, relief = 'flat')
        group2.pack(side = 'bottom', pady = 5, padx = 10)
        
        button4 = tk.Button(group2, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button4.pack(side = 'left', pady=5, padx=10)

        button5 = tk.Button(group2, text="Back to Admin",
                         command=lambda:controller.show_frame("Admin"))
        button5.pack(side = 'right', pady=5, padx=10)

class ModifySupplier(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        self.oldname = tk.StringVar()
        self.newname = tk.StringVar()
        self.var_message = tk.StringVar()
        
        label = tk.Label(self, text="Modify Supplier")
        label.pack(side = 'top', pady=10)

        group2 = tk.LabelFrame(self, relief = 'flat')
        group2.pack(side = 'top', pady = 5, padx = 10)
        
        labelold = tk.Label(group2, text = 'Current name: ')
        labelold.pack(side = 'left', pady=10)

        old = tk.Entry(group2)
        old['textvariable'] = self.oldname
        old.pack(side = 'left', pady = 10)
        
        group1 = tk.LabelFrame(self, relief = 'flat')
        group1.pack(side = 'top', pady = 5, padx = 10)
        
        labelnew = tk.Label(group1, text = 'New name: ')
        labelnew.pack(side = 'left', pady=10)

        new = tk.Entry(group1)
        new['textvariable'] = self.newname
        new.pack(side = 'left', pady = 10)
        
        # Message
        msg = tk.Message(self, width=500)
        msg['textvariable'] = self.var_message
        msg.pack(side = 'top', pady = 10)

        # Button
        confirm = tk.Button(self, text = "Confirm")
        confirm['command'] = lambda: self.change()
        confirm.pack(side = 'top', pady = 10)

        group3 = tk.LabelFrame(self, relief = 'flat')
        group3.pack(side = 'top', pady = 5, padx = 10)
        
        button2 = tk.Button(group3, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button2.pack(side = 'left', pady=5, padx=10)

        button3 = tk.Button(group3, text="Back to Suppliers",
                         command=lambda:controller.show_frame("Supplier"))
        button3.pack(side = 'right', pady=5, padx=10)

    def change(self):
        try:
            TUQ.update_row('supplier', {'supplier_name' : self.newname.get()}, {'supplier_name' : self.oldname.get()})
            self.var_message.set("Name of %s Updated to %s" % (self.oldname.get(), self.newname.get()))
            # Empty the entry fields
            self.oldname.set("")
            self.newname.set("")
        except:
            self.var_message.set("An Error occured during processing, not executed")
            
class AddSupplier(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        self.supplierid = tk.StringVar()
        self.supplier= tk.StringVar()
        self.var_message = tk.StringVar()
        
        label = tk.Label(self, text="Add Supplier")
        label.pack(side = 'top', pady=10)

        group2 = tk.LabelFrame(self, relief = 'flat')
        group2.pack(side = 'top', pady = 5, padx = 10)
        
        labelsup = tk.Label(group2, text = 'Supplier: ')
        labelsup.pack(side = 'left', pady=10)

        supplier = tk.Entry(group2)
        supplier['textvariable'] = self.supplier
        supplier.pack(side = 'left', pady = 10)

        # Message
        msg = tk.Message(self, width=500)
        msg['textvariable'] = self.var_message
        msg.pack(side = 'top', pady = 10)

        # Button
        confirm = tk.Button(self, text = "Add")
        confirm['command'] = lambda: self.popup()
        confirm.pack(side = 'top', pady = 10)


        group3 = tk.LabelFrame(self, relief = 'flat')
        group3.pack(side = 'top', pady = 5, padx = 10)
        
        button2 = tk.Button(group3, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button2.pack(side = 'left', pady=5, padx=10)

        button3 = tk.Button(group3, text="Back to Suppliers",
                         command=lambda:controller.show_frame("Supplier"))
        button3.pack(side = 'right', pady=5, padx=10)


    def popup(self):
        """ A popup window which asks to confirm action"""
        self.win = tk.Toplevel()

        label0 = tk.Label(self.win, text = ("Are you sure you want to add '%s' ?" % self.supplier.get()))
        label0.pack(side = 'top', pady = 5)

        buttongroup = tk.LabelFrame(self.win)
        buttongroup.pack(side = 'top')
      
        button1 = tk.Button(buttongroup, text = 'Confirm',
                            command = lambda : self.add())
        button1.pack(side = 'left', padx = 5, pady = 10)

        button2 = tk.Button(buttongroup, text = 'Cancel',
                            command = lambda : self.win.destroy())
        button2.pack(side = 'left', padx = 5, pady = 10)

    def add(self):
        """Add a supplier to supplier-table """

        # Get supplier name, check whether not empty
        suppliername = self.supplier.get()
        suppliername = suppliername.strip()
        if suppliername == "":
                self.var_message.set("Invalid name")
        else:
            db = MySQLdb.connect(cfg.mysql['host'], self.controller.shared_data["username"].get(),
                                 self.controller.shared_data["password"].get(), cfg.mysql['database']) # open connection
            cursor = db.cursor() # prepare a cursor object

            # Make a sql for creation of new user
            add_supp_sql = TUQ.make_insert_row('supplier', {'supplier_ID' : IOP.make_new_ID('supplier'), 'supplier_name' : suppliername})

            try:
                cursor.execute(add_supp_sql)
                db.commit()
                cursor.close()
                db.close()
                self.var_message.set("%s Added" % suppliername)
                self.win.destroy()
                
            except MySQLdb.Error,e:# Rollback in case there is any error
                db.rollback()
                cursor.close()
                db.close()
                self.var_message.set((e[0], e[1]))
        # Empty entry field
        self.supplier.set("")

#############################________________GENERAL ODERSTATUS________________#############################
        
class GeneralOrderStatus(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.batch = tk.StringVar()
        self.status = tk.StringVar()
        self.status.set("Delivered")
        self.message = tk.StringVar()

        label = tk.Label(self, text="Change Order Status")
        label.grid(row = 1, column = 1, columnspan=3, pady=10)

        label2 = tk.Label(self, text="batchnumber: ")
        label2.grid(row=2, column=2, pady=5, padx=10, sticky="WE")

        entry = tk.Entry(self, textvariable = self.batch)
        entry.grid(row = 2, column = 3)

        rb_ordered = tk.Radiobutton(self, text = "Ordered", activebackground = mycolor, selectcolor = 'black')
        rb_ordered['value'] = "Ordered"
        rb_ordered['variable'] = self.status
        rb_ordered['indicatoron'] = 2
        rb_ordered.grid(row=3, column=1,
                         sticky='W', padx=8)

        rb_delivery = tk.Radiobutton(self, text = "Delivered", activebackground = mycolor, selectcolor = 'black')
        rb_delivery['value'] = "Delivered"
        rb_delivery['variable'] = self.status
        rb_delivery['indicatoron'] = 2
        rb_delivery.grid(row=3, column=2,
                         sticky='W', padx=8)

        rb_stock = tk.Radiobutton(self, text = "Out of Stock", activebackground = mycolor, selectcolor = 'black')
        rb_stock['value'] = "Out of Stock"
        rb_stock['variable'] = self.status
        rb_stock['indicatoron'] = 2
        rb_stock.grid(row=3, column=3,
                         sticky='W', padx=8)
        
        msg = tk.Message(self, textvariable = self.message, width = 280)
        msg.grid(row=4, column = 2)

        button1 = tk.Button(self, text = "Confirm",
                           command = lambda : self.update_status())
        button1.grid(row = 5, column = 2, pady=5, padx=10)

        button2 = tk.Button(self, text="Back to Home",
                         command=lambda:self.controller.show_frame("Home"))
                            
        button2.grid(row=7, column=3, pady=5, padx=10)

        button3 = tk.Button(self, text = "Back to Admin",
                            command = lambda : self.controller.show_frame("Admin"))
        button3.grid(row=7, column=4, pady=5, padx=10)

    def update_status(self):
        try:
            # get current status
            batchstatus = TLQ.execute_select_queries("SELECT order_status FROM `batch` \
                                                     WHERE batch_number = '%s'" % self.batch.get())
        except:
            self.message.set("Could not retrieve current status")

        # if there is no error
        if self.message.get() != "Could not retrieve current status":
            try:
            # If current status is not equal to new status
                if batchstatus[0][0] != self.status.get():
                
                    TUQ.update_row('batch', {'order_status' : self.status.get()},
                               {'batch_number' : self.batch.get()})
                    self.message.set("Succesfull")
            except:
                self.message.set("An Error occured when trying to update status")
                
#############################________________EMPLOYEES________________#############################
                
class Employees(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="Employees")
        label.grid(row = 1, column = 1, columnspan=3, pady=10)

        button1 = tk.Button(self, text="View", bg=mycolor,
                            command = lambda : TLQ.build_query_and_table("employee"))
        
        button1.grid(row=2, column=2, pady=5, padx=10, sticky="WE")

        button2 = tk.Button(self, text="Add",
                            command = lambda : self.controller.show_frame('AddEmployee'))

        button2.grid(row=4, column=2, pady=5, padx=10, sticky="WE")

        button3 = tk.Button(self, text="Admin Rights",
                            command = lambda : self.controller.show_frame('AdminRights'))

        button3.grid(row=6, column=2, pady=5, padx=10, sticky="WE")


        button4 = tk.Button(self, text="Remove User",
                            command = lambda : self.controller.show_frame('RemoveUser'))

        button4.grid(row=8, column=2, pady=5, padx=10, sticky="WE")

        button5 = tk.Button(self, text="Back to Home",
                         command=lambda:self.controller.show_frame("Home"))
                            
        button5.grid(row=10, column=3, pady=5, padx=10)

        button6 = tk.Button(self, text = "Back to Admin",
                            command = lambda : self.controller.show_frame("Admin"))
        button6.grid(row=10, column=4, pady=5, padx=10)
        
                  
class AddEmployee(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        self.username = tk.StringVar()
        self.npassword = tk.StringVar()
        self.rnpassword = tk.StringVar()
        self.var_message = tk.StringVar()
        self.adminvalid = tk.IntVar()
        
        label = tk.Label(self, text="Add an Employee")
        label.pack(side = 'top', pady=10)

        # user
        group1 = tk.LabelFrame(self, relief = 'flat')
        group1.pack(side = 'top', pady = 10)
        
        usernamelabel = tk.Label(group1, text = "Username: ")
        usernamelabel.pack(side = 'left', padx = 5, pady=10)

        username = tk.Entry(group1)
        username['textvariable'] = self.username
        username.pack(side = 'right', padx = 5, pady = 10)
        
        # new password
        group2 = tk.LabelFrame(self, relief = 'flat')
        group2.pack(side = 'top', pady = 10)

        npwlabel = tk.Label(group2, text = "Password: ")
        npwlabel.pack(side = 'left', padx = 5, pady=10)

        npw = tk.Entry(group2, show = "*")
        npw['textvariable'] = self.npassword
        npw.pack(side = 'right', padx = 5, pady = 10)

        # repeat password
        group3 = tk.LabelFrame(self, relief = 'flat')
        group3.pack(side = 'top', pady = 10)
        
        rnlabel = tk.Label(group3, text = "Repeat Password: ")
        rnlabel.pack(side = 'left', padx = 5, pady=10)

        rnpw = tk.Entry(group3, show = "*")
        rnpw['textvariable'] = self.rnpassword
        rnpw.pack(side = 'right', padx = 5, pady = 10)

        admin = tk.Checkbutton(self, text = 'Admin', onvalue = 1, offvalue = 0, selectcolor = 'black')
        admin['variable'] = self.adminvalid
        admin.pack(side = 'top', pady = 10)

        # Message
        msg = tk.Message(self, width=280)
        msg['textvariable'] = self.var_message
        msg.pack(side = 'top', pady = 10)

        # Button
        changpass = tk.Button(self, text = "Confirm")
        changpass['command'] = lambda: self.insert_user()
        changpass.pack(side = 'top', pady = 10)

        group4 = tk.LabelFrame(self, relief = 'flat')
        group4.pack(side = 'top', pady = 10)

        button2 = tk.Button(group4, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button2.pack(side = 'left', pady = 5, padx=10)

        button3 = tk.Button(group4, text="Back to Employees",
                         command=lambda:controller.show_frame("Employees"))
        button3.pack(side = 'right', pady=5, padx=10)

    def insert_user(self):
        """Inserts a new employee"""
        
        # check new and repeat new are equel
        
        if self.npassword.get() != self.rnpassword.get():
            self.var_message.set("Passwords are not entered correctly")
        else:
            # remove trailing or leading spaces
            username = self.username.get()
            username = username.strip()
            # check whether they contain something
            if username == "" or self.npassword.get() == "":
                self.var_message.set("Invalid username or password")
            else:

                db = MySQLdb.connect(cfg.mysql['host'], self.controller.shared_data["username"].get(),
                                     self.controller.shared_data["password"].get(),
                                     cfg.mysql['database']) # open connection
                
                cursor = db.cursor() # prepare a cursor object

                # Make a sql for creation of new user
                create_user_sql = "CREATE USER %s@%s IDENTIFIED BY '%s'" % (username, cfg.mysql['hostadress'], self.npassword.get())

                # Make sql to grant rights/privileges to new user
                if self.adminvalid.get() == 1:
                    grant_sql = "Grant select, insert, reload, update, delete on *.* to %s@%s WITH GRANT OPTION" %(username, cfg.mysql['hostadress'])
                elif self.adminvalid.get() == 0:
                    grant_sql = "Grant select, insert, update, delete on %s.* to %s@%s" % (cfg.mysql['database'], username, cfg.mysql['hostadress'])

                # Make sql to add user to employee table
                insert_user_sql = TUQ.make_insert_row('Employee',{'employee_ID' : IOP.new_emp_ID('employee'), 'emp_name' : username, 'password' : self.npassword.get()})

                try:
                    cursor.execute(create_user_sql)
                    cursor.execute(grant_sql)
                    cursor.execute("FLUSH PRIVILEGES") # Refresh/save priviliges
                    cursor.execute(insert_user_sql)
                    db.commit()
                    cursor.close()
                    db.close()
                    self.var_message.set("Succesfully added %s" % self.username.get() )
                except MySQLdb.Error,e:# Rollback in case there is any error
                    db.rollback()
                    raise ValueError(e[0], e[1])
                    cursor.close()
                    db.close() #disconnect from server
        # Empty entry field
        self.username.set("")
        self.npassword.set("")
        self.rnpassword.set("")
        
class RemoveUser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        self.username = tk.StringVar()
        self.var_message = tk.StringVar()
        
        label = tk.Label(self, text="Remove User")
        label.pack(side = 'top', pady=20)

        group1 = tk.LabelFrame(self, relief = 'flat')
        group1.pack(side = 'top', padx = 5, pady = 10)
        
        labeluser = tk.Label(group1, text = 'Username: ')
        labeluser.pack(side = 'left', padx = 5, pady=10)

        username = tk.Entry(group1)
        username['textvariable'] = self.username
        username.pack(side = 'right', padx = 5, pady = 10)

        # Message
        msg = tk.Message(self, width=280)
        msg['textvariable'] = self.var_message
        msg.pack(side = 'top', pady = 10)

        # Button
        confirm = tk.Button(self, text = "Remove")
        confirm['command'] = lambda: self.popup()
        confirm.pack(side = 'top', pady = 10)

        group2 = tk.LabelFrame(self, relief = 'flat')
        group2.pack(side = 'bottom', padx = 5, pady = 10)
        
        button2 = tk.Button(group2, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button2.pack(side = 'left', pady=5, padx=10)

        button3 = tk.Button(group2, text="Back to Employee",
                         command=lambda:controller.show_frame("Employees"))
        button3.pack(side = 'right', pady=5, padx=10)


    def popup(self):
        """ A popup window which asks to confirm action"""
        
        self.win = tk.Toplevel()

        label0 = tk.Label(self.win, text = ("Are you sure you want to remove '%s' ?" % self.username.get()))
        label0.pack(side = 'top', pady = 5)

        buttongroup = tk.LabelFrame(self.win, relief = 'flat')
        buttongroup.pack(side = 'top')
      
        button1 = tk.Button(buttongroup, text = 'Confirm',
                            command = lambda : self.remove())
        button1.pack(side = 'left', padx = 5, pady = 10)

        button2 = tk.Button(buttongroup, text = 'Cancel',
                            command = lambda : self.win.destroy())
        button2.pack(side = 'left', padx = 5, pady = 10)

    def remove(self):
        """Removes a User/employee login specifications, but not from the employee_table! """
        self.win.destroy()
        # Exectue only when the input username is not the same as the current user       
        if self.username.get() != self.controller.shared_data["username"].get():
        
            db = MySQLdb.connect(cfg.mysql['host'], self.controller.shared_data["username"].get(),
                                 self.controller.shared_data["password"].get(), cfg.mysql['database']) # open connection
            cursor = db.cursor() # prepare a cursor object

            # Make a sql for creation of new user
            drop_user_sql = "DROP USER %s@%s" % (self.username.get(), cfg.mysql['hostadress'])
            remove_password = TUQ.make_update_row('Employee', { 'password' : "" },
                                                           {'emp_name' : self.username.get()})
            try:
                cursor.execute(drop_user_sql)
                cursor.execute(remove_password)
                db.commit()
                self.var_message.set("%s Removed" % self.username.get())
                cursor.close()
                db.close()
                # Empty entry field
                self.username.set("")
            except MySQLdb.Error,e:# Rollback in case there is any error
                db.rollback()
                self.var_message.set(e[0], e[1])
                cursor.close()
                db.close() #disconnect from server
        else:
            self.var_message.set("Cannot remove your own user-account")
        
class AdminRights(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        self.username = tk.StringVar()
        self.var_message = tk.StringVar()
        
        label = tk.Label(self, text="Give or Revoke Admin Rights")
        label.grid(row = 1, column = 1, columnspan=8, pady=10)

        labeluser = tk.Label(self, text = 'Username: ')
        labeluser.grid(row = 3, column = 4, pady=10)

        username = tk.Entry(self)
        username['textvariable'] = self.username
        username.grid(row = 3, column = 6, columnspan = 4, pady = 10)

        # Message
        msg = tk.Message(self, width=280)
        msg['textvariable'] = self.var_message
        msg.grid(row=7, column=2, columnspan=4, pady = 10)

        # Button
        give = tk.Button(self, text = "Give Rights")
        give['command'] = lambda: self.giverights()
        give.grid(row = 8, column = 4, pady = 10)


        revoke = tk.Button(self, text = "Revoke Rights")
        revoke['command'] = lambda: self.revokerights()
        revoke.grid(row = 8, column = 6, pady = 10)


        button2 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("Home"))
        button2.grid(row=10, column=9, pady=5, padx=10, sticky="EW")

    def revokerights(self):
        """Removes the Admin rights of a user, and gives standard rights"""
        # Exectue only when the input username is not the same as the current user       
        if self.username.get() != self.controller.shared_data["username"].get():
            
            db = MySQLdb.connect(cfg.mysql['host'], self.controller.shared_data["username"].get(),
                                 self.controller.shared_data["password"].get(), cfg.mysql['database']) # open connection
            cursor = db.cursor() # prepare a cursor object
              
            # Make a sql to revoke all
            revoke_sql = "REVOKE ALL, GRANT OPTION FROM %s@%s" % (self.username.get(),
                                                                  cfg.mysql['hostadress'])

            # Make sql to grant the other rights again
            grant_sql = "Grant select, insert, update, delete on %s.* to %s@%s" %(cfg.mysql['database'],
                                                                                  self.username.get(), cfg.mysql['hostadress'])

            try:
                cursor.execute(revoke_sql)
                cursor.execute(grant_sql)
                cursor.execute("FLUSH PRIVILEGES")
                db.commit()
                cursor.close()
                db.close()
                self.var_message.set("Revoked Admin Rights of %s" % self.username.get())
            except MySQLdb.Error,e:# Rollback in case there is any error
                db.rollback()
                raise ValueError(e[0], e[1])
                cursor.close()
                db.close() #disconnect from server

            # Empty entry field
            self.username.set("")
        else:
            self.var_message.set("Cannot revoke your own rights")

    def giverights(self):
        """Replaces standard rights with Admin Rights"""

        db = MySQLdb.connect(cfg.mysql['host'], self.controller.shared_data["username"].get(),
                             self.controller.shared_data["password"].get(), cfg.mysql['database']) # open connection
        cursor = db.cursor() # prepare a cursor object

        # Make sql to grant the admin rights 
        grant_sql = "GRANT select, insert, reload, update, delete on *.* to %s@%s WITH GRANT OPTION" %(self.username.get(),
                                                                                               cfg.mysql['hostadress'])

        try:
            cursor.execute(grant_sql)
            cursor.execute("FLUSH PRIVILEGES")
            db.commit()
            cursor.close()
            db.close()
            self.var_message.set("Granted Admin Rights to %s" % self.username.get())
        except MySQLdb.Error,e:# Rollback in case there is any error
            db.rollback()
            raise ValueError(e[0], e[1])
            cursor.close()
            db.close() #disconnect from server

        # Empty entry field
        self.username.set("")

class OrderBin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="Order Bin")
        label.grid(row = 1, column = 1, columnspan=3, pady=10)

        button1 = tk.Button(self, text="View Order Bin", bg=mycolor,
                            command = lambda : TLQ.build_query_and_table('order_bin'))
        
        button1.grid(row=2, column=2, pady=5, padx=10, sticky="WE")

        button2 = tk.Button(self, text="Empty Order Bin",
                            command = lambda : self.popup())

        button2.grid(row=4, column=2, pady=5, padx=10, sticky="WE")


        button4 = tk.Button(self, text="Back to Home",
                         command=lambda:self.controller.show_frame("Home"))
                            
        button4.grid(row=9, column=3, pady=5, padx=10)

        button5 = tk.Button(self, text = "Back to Admin",
                            command = lambda : self.controller.show_frame("Admin"))
        button5.grid(row=9, column=4, pady=5, padx=10)
        
    
    def popup(self):
        self.win = tk.Toplevel()

        self.password = tk.StringVar()
        self.var_message = tk.StringVar()

        label0 = tk.Label(self.win, text = "Are you sure you want to remove all data from the Order-Bin?")
        label0.pack(side = 'top', pady = 5)

        buttongroup = tk.LabelFrame(self.win)
        buttongroup.pack(side = 'top')
      
        button1 = tk.Button(buttongroup, text = 'Confirm',
                            command = lambda : self.empty())
        button1.pack(side = 'left', padx = 5, pady = 10)

        button2 = tk.Button(buttongroup, text = 'Cancel',
                            command = lambda : self.win.destroy())
        button2.pack(side = 'left', padx = 5, pady = 10)

    def empty(self):
        TUQ.empty_bin()
        self.var_message.set("Bin is being emptied, please wait")
        self.win.destroy()
            
#############################________________ORDER STATUS________________#############################
            


class OrderStatus(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller

        label = tk.Label(self, text="Order Status")
        label.grid(row = 1, column = 1, columnspan=3, pady=10)

        button1 = tk.Button(self, text="Order Queue", bg=mycolor,
                            command = lambda : self.controller.show_frame("OrderQueue"))
        
        button1.grid(row=2, column=2, pady=5, padx=10, sticky="WE")

        button2 = tk.Button(self, text="Deliveries",
                            command = lambda : self.controller.show_frame("Deliveries"))

        button2.grid(row=3, column=2, pady=5, padx=10, sticky="WE")

        button3 = tk.Button(self, text="Out of Stock",
                            command = lambda : self.controller.show_frame("OutOfStock"))
        
        button3.grid(row=4, column=2, pady=5, padx=10, sticky="WE")

        button4 = tk.Button(self, text="Back to Home",
                         command=lambda:self.controller.show_frame("Home"))
                            
        button4.grid(row=9, column=3, pady=5, padx=10)

#############################________________ORDER QUEUE________________#############################

class OrderQueue(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller

        label = tk.Label(self, text="Order Queue")
        label.grid(row = 1, column = 1, columnspan=3, pady=10)

        button1 = tk.Button(self, text="View Queue", bg=mycolor,
                            command = lambda : TLQ.build_query_and_table('order_queue'))
        
        button1.grid(row=2, column=2, pady=5, padx=10, sticky="WE")

        button2 = tk.Button(self, text="View Bin",
                            command = lambda : TLQ.build_query_and_table('order_bin'))

        button2.grid(row=4, column=2, pady=5, padx=10, sticky="WE")

        button3 = tk.Button(self, text="Move to Bin",
                            command = lambda : self.controller.show_frame("QueueToBin"))
        button3.grid(row=2, column=3, pady=5, padx=10, sticky="WE")

        button4 = tk.Button(self, text="Move to Queue",
                            command = lambda : self.controller.show_frame("BinToQueue"))
        button4.grid(row=4, column=3, pady=5, padx=10, sticky="WE")

        button5 = tk.Button(self, text="Process Queue",
                            command = lambda: self.controller.show_frame('ProcessQueue'))
        button5.grid(row=6, column=2, pady=5, padx=10, sticky="WE")

        button6 = tk.Button(self, text="Back to Home",
                         command=lambda:self.controller.show_frame("Home"))
                            
        button6.grid(row=9, column=4, pady=5, padx=10)

        button7 = tk.Button(self, text="Back to Order Status",
                         command=lambda:self.controller.show_frame("OrderStatus"))
                            
        button7.grid(row=9, column=5, pady=5, padx=10)

class BinToQueue(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        self.Text = None
        self.message = tk.StringVar()

        label = tk.Label(self, text="Move from Bin to Queue")
        label.pack(side = 'top', pady=10)


        label1 = tk.Label(self, text="Enter the bin_ID('s) : ")
        label1.pack(side = 'top', pady=5)

        self.Text = tk.Text(self, width = 30, height = 10)
        self.Text.pack(side = 'top', pady = 5)

        message = tk.Message(self, textvariable = self.message, width = 280)
        message.pack(side = 'top')

        button = tk.Button(self, text = 'Move oligos(s) back to order queue')
        button['command'] = lambda : self.move()
        button.pack(side = 'top', pady = 10)

        buttongroup = tk.LabelFrame(self)
        buttongroup.pack(side = 'top')
        
        button2 = tk.Button(buttongroup, text = 'Back to Home',
                            command = lambda : self.controller.show_frame("Home"))
        button2.pack(side = 'left', pady=5, padx = 5)

        button3 = tk.Button(buttongroup, text = 'Back to Order Queue',
                             command = lambda : self.controller.show_frame("OrderQueue"))
        button3.pack(side = 'left', pady=5, padx = 5)


    def move(self):
        text = self.gettext()
        text = text.split()
        try:
            for id_ in text:
                TUQ.move_row(id_, 'order_bin', 'order_queue')
            self.message.set('Move succesfull')
        except MySQLdb.Error,e: 
            self.var_message.set((e[0], e[1]))

    def gettext(self):
        text = self.Text.get(1.0, tk.END)
        if text is not None:
            text = text.strip()
        if  text == "":
            text = None
        return text

class QueueToBin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        self.Text = None
        self.message = tk.StringVar()

        label = tk.Label(self, text="Move from Queue to Bin")
        label.pack(side = 'top', pady=10)


        label1 = tk.Label(self, text="Enter the queue ID('s) : ")
        label1.pack(side = 'top', pady=5)

        self.Text = tk.Text(self, width = 30, height = 10)
        self.Text.pack(side = 'top', pady = 5)

        message = tk.Message(self, textvariable = self.message, width = 280)
        message.pack(side = 'top')

        button = tk.Button(self, text = 'Remove oligo(s) from queue')
        button['command'] = lambda : self.move()
        button.pack(side = 'top', pady = 10)

        buttongroup = tk.LabelFrame(self, relief = 'flat')
        buttongroup.pack(side = 'top')
        
        button2 = tk.Button(buttongroup, text = 'Back to Home',
                            command = lambda : self.controller.show_frame("Home"))
        button2.pack(side = 'left', pady=5, padx = 5)

        button3 = tk.Button(buttongroup, text = 'Back to Order Queue',
                             command = lambda : self.controller.show_frame("OrderQueue"))
        button3.pack(side = 'left', pady=5, padx = 5)


    def move(self):
        text = self.gettext()
        text = text.split()
        try:
            for id_ in text:
                TUQ.move_row(id_, 'order_queue', 'order_bin')
            self.message.set('Move succesfull')
        except MySQLdb.Error,e: 
            self.var_message.set('An Error occured')

    def gettext(self):
        text = self.Text.get(1.0, tk.END)
        if text is not None:
            text = text.strip()
        if  text == "":
            text = None
        return text

class ProcessQueue(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        self.Text = None
        self.message = tk.StringVar()

        label = tk.Label(self, text="Process Queue to database")
        label.pack(side = 'top', pady=10)


        label1 = tk.Label(self, text="Enter the queue ID('s) that you want to process : ")
        label1.pack(side = 'top', pady=5)

        self.Text = tk.Text(self, width = 30, height = 10)
        self.Text.pack(side = 'top', pady = 5)

        message = tk.Message(self, textvariable = self.message, width = 280)
        message.pack(side = 'top')

        processbutton = tk.Button(self, text = 'Process oligo(s)')
        processbutton['command'] = lambda : self.process()
        processbutton.pack(side = 'top', pady = 10)

        buttongroup = tk.LabelFrame(self)
        buttongroup.pack(side = 'top')
        
        button2 = tk.Button(buttongroup, text = 'Back to Home',
                            command = lambda : self.controller.show_frame("Home"))
        button2.pack(side = 'left', pady=5, padx = 5)

        button3 = tk.Button(buttongroup, text = 'Back to Order Queue',
                             command = lambda : self.controller.show_frame("OrderQueue"))
        button3.pack(side = 'left', pady=5, padx = 5)

        # Button
        #confirm = tk.Button(self, text = "Add")
        #confirm['command'] = lambda: self.popup()
        #confirm.pack(side = 'top', pady = 10)


    def popup(self):
        """ A popup window which asks to confirm action"""
        self.win = tk.Toplevel()

        label0 = tk.Label(self.win, text = " The sequence and labels are duplicated \n \
Do you want to import anyway? \n A new batchno will be created")
        label0.pack(side = 'top', pady = 5)

        buttongroup = tk.LabelFrame(self.win)
        buttongroup.pack(side = 'top')
      
        button1 = tk.Button(buttongroup, text = 'Yes',
                            command = lambda : self.confirm("y"))
        button1.pack(side = 'left', padx = 5, pady = 10)

        button2 = tk.Button(buttongroup, text = 'No',
                            command = lambda : self.win.destroy())
        button2.pack(side = 'left', padx = 5, pady = 10)

    def confirm(self, yesorno):
        answer = yesorno
        return answer
        
    def process(self):
        text = self.gettext()
        text = text.split()
        #try: 
        IOP.process_to_db(self, text)
            #self.message.set('suppliers are the same, starting process')
        #except:
          #  self.message.set('two or more suppliers provided, not able to process')


    def gettext(self):
        text = self.Text.get(1.0, tk.END)
        if text is not None:
            text = text.strip()
        if  text == "":
            text = None
        return text
    

#############################________________DELIVERIES________________#############################

class Deliveries(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        self.batch = tk.StringVar()
        self.synth = tk.StringVar()
        self.message = tk.StringVar()

        label = tk.Label(self, text="Enter new Delivery")
        label.grid(row = 0, column = 2, pady=10)


        label1 = tk.Label(self, text="Enter the Batchnumber('s) : ")
        label1.grid(row = 1, column = 1, pady=5)

        batchlabel = tk.Label(self, text = "Batchnumber: ")
        batchlabel.grid(row = 3, column = 1, pady = 5)

        batchentry = tk.Entry(self, textvariable = self.batch)
        batchentry.grid(row = 3, column = 2, pady = 5)

        synthlabel = tk.Label(self, text = "Delivery synthesis level: ")
        synthlabel.grid(row = 4, column = 1, pady = 5)
        
        synthentry = tk.Entry(self, textvariable = self.synth)
        synthentry.grid(row = 4, column = 2, pady = 5)
        
        message = tk.Message(self, textvariable = self.message, width = 280)
        message.grid(row = 5, column = 1, columnspan = 4)

        button = tk.Button(self, text = 'Confirm Delivery')
        button['command'] = lambda : self.update_status()
        button.grid(row = 6, column = 2, pady = 10)

        buttongroup = tk.LabelFrame(self)
        buttongroup.grid(row = 7, column = 2)
        
        button2 = tk.Button(buttongroup, text = 'Back to Home',
                            command = lambda : self.controller.show_frame("Home"))
        button2.pack(side = 'left', pady=5, padx = 5)

        button3 = tk.Button(buttongroup, text = 'Back to Order Status',
                             command = lambda : self.controller.show_frame("OrderStatus"))
        button3.pack(side = 'left', pady=5, padx = 5)


    def update_status(self):
        try:
            batchstatus = TLQ.execute_select_queries("SELECT order_status FROM `batch` \
                                                     WHERE batch_number = '%s'" % self.batch.get())
            if batchstatus[0][0] == 'Ordered':
                TUQ.update_row('batch', {'synthesis_level_delivered' : self.synth.get(), 'order_status' : 'Delivered',
                                     'delivery_date' : IOP.get_date_stamp()}, {'batch_number' : self.batch.get()})
                self.message.set("Succesfull")
        except:
            self.message.set("An Error occured, please try again")

#############################________________OUT OF STOCK________________#############################

class OutOfStock(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        self.Text = None
        self.message = tk.StringVar()

        label = tk.Label(self, text="Set batches to be 'Out of Stock'")
        label.pack(side = 'top', pady=10)


        label1 = tk.Label(self, text="Enter the batchnumber('s) : ")
        label1.pack(side = 'top', pady=5)

        self.Text = tk.Text(self, width = 30, height = 10)
        self.Text.pack(side = 'top', pady = 5)

        message = tk.Message(self, textvariable = self.message, width = 280)
        message.pack(side = 'top')

        button = tk.Button(self, text = 'Confirm')
        button['command'] = lambda : self.update_status()
        button.pack(side = 'top', pady = 10)

        buttongroup = tk.LabelFrame(self)
        buttongroup.pack(side = 'top')
        
        button2 = tk.Button(buttongroup, text = 'Back to Home',
                            command = lambda : self.controller.show_frame("Home"))
        button2.pack(side = 'left', pady=5, padx = 5)

        button3 = tk.Button(buttongroup, text = 'Back to Order Queue',
                             command = lambda : self.controller.show_frame("OrderQueue"))
        button3.pack(side = 'left', pady=5, padx = 5)
      
    def update_status(self):
        try:
            text = self.gettext()
            text = text.split()
            for batch in text:
                batchstatus = TLQ.execute_select_queries("SELECT order_status FROM `batch` \
                                                     WHERE batch_number = '%s'" % batch)
                if batchstatus[0][0] == 'Delivered':
                    TUQ.update_row('batch', {'order_status' : 'Out of Stock'}, {'batch_number' : batch})
                    self.message.set("Succesfull")
        except:
            self.message.set("An Error occured, please try again")

    def gettext(self):
        text = self.Text.get(1.0, tk.END)
        if text is not None:
            text = text.strip()
        if  text == "":
            text = None
        return text
                    
####################################
        ##################
        ############
    
#############################________________OLD PAGES________________#############################
        
class ProjectsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="Projects menu")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)

        

class EmployeesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="Employees menu")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)


class BatchesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="Batches menu")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)

class SuppliersPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="Suppliers menu")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)


class ExperimentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        
        
        label = tk.Label(self, text="Experiment menu")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)

        button2 = tk.Button(self, text="View All Experiments",
                         command=lambda:controller.show_frame("ViewExperimentPage"))

                             #show a table view of all experiments
        button2.grid(row=4, column=2, pady=5, padx=10, sticky="WE")

        button3 = tk.Button(self, text="New Experiment",
                        command=lambda:controller.show_frame("NewExperimentPage"))
                             #show some text fields for adding experiments
        button3.grid(row=6, column=2, pady=5, padx=10, sticky="WE")

        button4 = tk.Button(self, text="Edit Experiment",
                        command=lambda:controller.show_frame("EditExperimentPage"))
                             #show text fields where you can browse for experiment
        button4.grid(row=4, column=4, pady=5, padx=10, sticky="WE")

        button5 = tk.Button(self, text="Lookup Experiment",
                        command=lambda:controller.show_frame("LookupExperimentPage"))
        button5.grid(row=6, column=4, pady=5, padx=10, sticky="WE")


class ViewExperimentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="View Experiment")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)

        button2 = tk.Button(self, text="Back to Experiments",
                         command=lambda:controller.show_frame("ExperimentPage"))
        button2.grid(row=6, column=8, pady=5, padx=10)

class NewExperimentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="New Experiment")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button1.grid(row=10, column=7, pady=5, padx=10)

        button2 = tk.Button(self, text="Back to Experiments",
                         command=lambda:controller.show_frame("ExperimentPage"))
        button2.grid(row=9, column=7, pady=5, padx=10)

        button3 = tk.Button(self, text="Continue",
                            command=lambda:controller.show_frame(
                                "ContinueNewExperimentPage"))
        button3.grid(row=9, column=6, pady=5, padx=10)

        #Experiment_ID label+entry
        label1 = tk.Label(self, text="Experiment_ID: ")
                        #command = self generated a new number
        label1.grid(row=3, column=2, sticky="E")

        entry1 = tk.Entry(self, bg='white', fg='black', width=30)
        entry1.grid(row=3, column=3, sticky="NSEW")

        # Project label+entry
        label2 = tk.Label(self, text="Project: ")
        label2.grid(row=3, column=5, sticky="E")

        entry2 = tk.Entry(self, bg='white', fg='black', width=30)
        entry2.grid(row=3, column=6, sticky="NSEW")

        # Oligo 1 label + 3 entry fields        
        label3 = tk.Label(self, text="Oligo 1")
        label3.grid(row=5, column=2, sticky="EW")

        entry3_1 = tk.Entry(self, bg='white', fg='black', width=30)
        entry3_1.grid(row=6, column=2, sticky="EW")

        entry3_2 = tk.Entry(self, bg='white', fg='black', width=30)
        entry3_2.grid(row=7, column=2, sticky="EW")

        entry3_3 = tk.Entry(self, bg='white', fg='black', width=30)
        entry3_3.grid(row=8, column=2, sticky="EW") 

        # Oligo 2 label + 3 entry fields        
        label4 = tk.Label(self, text="Oligo 2")
        label4.grid(row=5, column=4, sticky="EW")

        entry4_1 = tk.Entry(self, bg='white', fg='black', width=30)
        entry4_1.grid(row=6, column=4, sticky="EW")

        entry4_2 = tk.Entry(self, bg='white', fg='black', width=30)
        entry4_2.grid(row=7, column=4, sticky="EW")

        entry4_3 = tk.Entry(self, bg='white', fg='black', width=30)
        entry4_3.grid(row=8, column=4, sticky="EW")

        # Oligo 3 label + 3 entry fields        

        label5 = tk.Label(self, text="Oligo 3")
        label5.grid(row=5, column=6, sticky="EW")

        entry5_1 = tk.Entry(self, bg='white', fg='black', width=30)
        entry5_1.grid(row=6, column=6, sticky="EW")

        entry5_2 = tk.Entry(self, bg='white', fg='black', width=30)
        entry5_2.grid(row=7, column=6, sticky="EW")

        entry5_3 = tk.Entry(self, bg='white', fg='black', width=30)
        entry5_3.grid(row=8, column=6, sticky="EW")

class ContinueNewExperimentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="New Experiment (continued)")
        label.grid(columnspan=8, pady=10)


        button1 = tk.Button(self, text="Back to Experiments Home",
                         command=lambda:controller.show_frame("ExperimentPage"))
        button1.grid(row=15, column=7, pady=5, padx=10)

        button2 = tk.Button(self, text="Back to Experiment",
                         command=lambda:controller.show_frame("NewExperimentPage"))
        button2.grid(row=14, column=7, pady=5, padx=10)

        button3 = tk.Button(self, text="Upload")
                            #command to upload the experiment to database
        button3.grid(row=13, column=6, pady=5, padx=10)

        # Experiment_ID label and entry
        label1 = tk.Label(self, text="Experiment_ID: ")
        label1.grid(row=2, column=2, sticky="EW")

        entry1 = tk.Entry(self, bg='white', fg='black', width=30)
        entry1.grid(row=2, column=3, sticky="NSEW")

        # Oligo 1 label 
        label1 = tk.Label(self, text="Oligo 1")
        label1.grid(row=3, column=2, sticky="EW")

        entry1_1 = tk.Entry(self, bg='white', fg='black', width=30)
        entry1_1.grid(row=4, column=2, sticky="EW")

        entry1_2 = tk.Entry(self, bg='white', fg='black', width=30)
        entry1_2.grid(row=7, column=2, sticky="EW")

        entry1_3 = tk.Entry(self, bg='white', fg='black', width=30)
        entry1_3.grid(row=10, column=2, sticky="EW")
        
        # Oligo 2 label 
        label2 = tk.Label(self, text="Oligo 2")
        label2.grid(row=3, column=3, sticky="EW")

        entry2_1 = tk.Entry(self, bg='white', fg='black', width=30)
        entry2_1.grid(row=4, column=3, sticky="EW")

        entry2_2 = tk.Entry(self, bg='white', fg='black', width=30)
        entry2_2.grid(row=5, column=3, sticky="EW")

        entry2_3 = tk.Entry(self, bg='white', fg='black', width=30)
        entry2_3.grid(row=6, column=3, sticky="EW")

        entry2_4 = tk.Entry(self, bg='white', fg='black', width=30)
        entry2_4.grid(row=7, column=3, sticky="EW")

        entry2_5 = tk.Entry(self, bg='white', fg='black', width=30)
        entry2_5.grid(row=8, column=3, sticky="EW")

        entry2_6 = tk.Entry(self, bg='white', fg='black', width=30)
        entry2_6.grid(row=9, column=3, sticky="EW")

        entry2_7 = tk.Entry(self, bg='white', fg='black', width=30)
        entry2_7.grid(row=10, column=3, sticky="EW")

        entry2_8 = tk.Entry(self, bg='white', fg='black', width=30)
        entry2_8.grid(row=11, column=3, sticky="EW")

        entry2_9 = tk.Entry(self, bg='white', fg='black', width=30)
        entry2_9.grid(row=12, column=3, sticky="EW")

        # Oligo 3 label 
        label4 = tk.Label(self, text="Oligo 3")
        label4.grid(row=3, column=4, sticky="EW")

        entry4_1 = tk.Entry(self, bg='white', fg='black', width=30)
        entry4_1.grid(row=6, column=4, sticky="EW")

        entry4_2 = tk.Entry(self, bg='white', fg='black', width=30)
        entry4_2.grid(row=8, column=4, sticky="EW")


class EditExperimentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="Edit Experiment")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)

        button2 = tk.Button(self, text="Back to Experiments",
                         command=lambda:controller.show_frame("ExperimentPage"))
        button2.grid(row=6, column=8, pady=5, padx=10)

class LookupExperimentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="Lookup Experiment")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)

        button2 = tk.Button(self, text="Back to Experiments",
                         command=lambda:controller.show_frame("ExperimentPage"))
        button2.grid(row=6, column=8, pady=5, padx=10)



if __name__ == "__main__":
    app = OligoDatabase()
    app.mainloop()
