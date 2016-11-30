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
import os
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
                  BatchesPage, SuppliersPage, ExperimentPage,
                  ViewAllOligos, NewOligo, ModifyOligo, LookupOligo,
                  ViewExperimentPage, NewExperimentPage, EditExperimentPage,
                  LookupExperimentPage, ContinueNewExperimentPage):
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
                        command=lambda:controller.show_frame("ExperimentPage"))
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

        button4 = tk.Button(self, text="Lookup Oligo",
                        command=lambda:controller.show_frame("LookupOligo"))
                            #goes to table view of one oligo
        button4.grid(row=4, column=4, pady=5, padx=10, sticky="EW")

        button5 = tk.Button(self, text="Modify Oligo",
                        command=lambda:controller.show_frame("ModifyOligo"))

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

        button2 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button2.grid(row=10, column=9, pady=5, padx=10, sticky="EW")

class NewOligo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        path_var = tk.StringVar()
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

        text_path = tk.Entry(self, bg='white', fg='black', width=50,
                             textvariable=path_var, justify="left" )
                                # add feature that it will expand upon selection
        text_path.grid(row=8, column=3, columnspan=4)

        button3 = tk.Button(self, text="Browse",
                            command=lambda:path_var.set(askopenfilename()))
        button3.grid(row=8, column=7)

        button4 = tk.Button(self, text="Upload")
                            #command = Uploads the file in the path into the
                            # specified columns of the db
        button4.grid(row=8, column=8)

        
class LookupOligo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="Lookup Oligos")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Oligo Menu",
                         command=lambda:controller.show_frame("OligosPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)

        button2 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button2.grid(row=10, column=9, pady=5, padx=10, sticky="EW")

class ModifyOligo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #save a reference to controller in each page:
        self.controller = controller

        
        label = tk.Label(self, text="Modify Oligos")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Oligo Menu",
                         command=lambda:controller.show_frame("OligosPage"))
        button1.grid(row=8, column=8, pady=5, padx=10)

        button2 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame("StartPage"))
        button2.grid(row=10, column=9, pady=5, padx=10, sticky="EW")

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
        button1.grid(row=8, column=7, pady=5, padx=10)

        button2 = tk.Button(self, text="Back to Experiment",
                         command=lambda:controller.show_frame("NewExperimentPage"))
        button2.grid(row=9, column=7, pady=5, padx=10)

        button3 = tk.Button(self, text="Upload")
                            #command to upload the experiment to database
        button3.grid(row=9, column=7, pady=5, padx=10)

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
