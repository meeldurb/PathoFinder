"""Author: Melanie van den Bosch
Jorn van der Ent
Script for having multiple windows frames in a GUI
"""


## When you want to add a page, simply create a new class
## put the page its classname inside the Frames for-loop
## and add the page in the Startpage class under commands
from __future__ import division
import math
import sys
import Tkinter as tk
import tkFont
from tkFileDialog import askopenfilename



mycolor = '#%02x%02x%02x' % (0, 182, 195)


class OligoDatabase(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # setting a default font for complete GUI
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Corbel", size=24)
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

        for F in (StartPage, OligosPage, ProjectsPage, EmployeesPage,
                  BatchesPage, SuppliersPage, ExperimentsPage,
                  ViewAllOligos, NewOligo):
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
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """ Raises the frame of the given page name to the top
        """
        frame = self.frames[page_name]
        frame.tkraise() 

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        # each page is a subblass of tk.Frame class, this calls
        # constructor of parent class
        # necessary to initialize internal structures that make up frame widget
        # send in a ref to another widget which is to act as the parent
        # of this new widget
        tk.Frame.__init__(self, parent)


        #save a reference to controller in each page:
        self.controller = controller
        

        label = tk.Label(self, text="Home")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Oligos", bg=mycolor,
                            command=lambda:controller.show_frame("OligosPage"))
        button1.grid(row=2, column=2, pady=5, padx=10, sticky="WE")

        button2 = tk.Button(self, text="Projects",
                         command=lambda:controller.show_frame("ProjectsPage"))
        button2.grid(row=4, column=2, pady=5, padx=10, sticky="WE")

        button3 = tk.Button(self, text="Employees",
                        command=lambda:controller.show_frame("EmployeesPage"))
                             # go to Employees page
        button3.grid(row=6, column=2, pady=5, padx=10, sticky="WE")

        button4 = tk.Button(self, text="Batches",
                        command=lambda:controller.show_frame("BatchesPage"))
        button4.grid(row=2, column=4, pady=5, padx=10, sticky="EW")

        button5 = tk.Button(self, text="Suppliers",
                        command=lambda:controller.show_frame("SuppliersPage"))
        button5.grid(row=4, column=4, pady=5, padx=10, sticky="EW")

        button6 = tk.Button(self, text="Experiments",
                        command=lambda:controller.show_frame("ExperimentsPage"))
                            # go to Experiments page
        button6.grid(row=6, column=4, pady=5, padx=10, sticky="EW")

        button7 = tk.Button(self, text="Quit", command=controller.destroy)
                            # Close the program
        button7.grid(row=8, column=8, pady=5, padx=10)

        
class OligosPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="Oligo Menu")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)

        button2 = tk.Button(self, text="View All Oligos",
                        command=lambda:controller.show_frame("ViewAllOligos"))
                            #Put here the table view that Jorn made
        button2.grid(row=4, column=2, pady=5, padx=10, sticky="WE")

        button3 = tk.Button(self, text="New Oligo",
                            command=lambda:controller.show_frame("NewOligo"))
                            #goes to new screen with textfields
        button3.grid(row=6, column=2, pady=5, padx=10, sticky="WE")

        button4 = tk.Button(self, text="Lookup Oligo")
                            #goes to table view of one oligo
        button4.grid(row=4, column=4, pady=5, padx=10, sticky="EW")

        button5 = tk.Button(self, text="Modify Oligo")
                            #gos to table view with textfields
        button5.grid(row=6, column=4, pady=5, padx=10, sticky="EW")
        
class ViewAllOligos(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="View All Oligos")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Oligo Menu",
                         command=lambda:controller.show_frame("OligosPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)

class NewOligo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="Entry of New Oligos")
        label.grid(row=1, columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Oligo Menu",
                         command=lambda:controller.show_frame("OligosPage"))
        button1.grid(row=9, column=9, pady=5, padx=10, sticky="EW")

        button2 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button2.grid(row=10, column=9, pady=5, padx=10, sticky="EW")

        label1 = tk.Label(self, text="Order number:")
        label1.grid (row=2, column=1)
        
        label2 = tk.Label(self, text="Import from file at location:")
        label2.grid(row=8, column=1, pady=5, padx=10)

        entry_text = tk.Entry(self, width=40)
        entry_text.grid(row=8, column=3, columnspan=4, rowspan=1, sticky="NS")

        button3 = tk.Button(self, text="Browse",
                            command=self.browse2file)
        button3.grid(row=8, column=7)

        button4 = tk.Button(self, text="Upload")
                            #command = Uploads the file in the path into the
                            # specified columns of the db
        button4.grid(row=8, column=8)

    def browse2file(self):
        filename = askopenfilename()

        

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


class ExperimentsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller
        
        
        label = tk.Label(self, text="Experiments menu")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)

        button2 = tk.Button(self, text="View All Experiments")
                             #show a table view of all experiments
        button2.grid(row=4, column=2, pady=5, padx=10, sticky="WE")

        button3 = tk.Button(self, text="New Experiment")
                             #show some text fields for adding experiments
        button3.grid(row=6, column=2, pady=5, padx=10, sticky="WE")

        button4 = tk.Button(self, text="Edit Experiments")
                             #show text fields where you can browse for experiment
        button4.grid(row=4, column=4, pady=5, padx=10, sticky="WE")

        button5 = tk.Button(self, text="Lookup")
                             #show text fields where you can lookup
        button5.grid(row=6, column=4, pady=5, padx=10, sticky="WE")




if __name__ == "__main__":
    app = OligoDatabase()
    app.mainloop()
