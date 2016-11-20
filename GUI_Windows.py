"""Author: Melanie van den Bosch
Jorn van der Ent
Script for having multiple windows frames in a GUI"""

from __future__ import division
import math 
import Tkinter as tk
import tkFont

#helv36 = tkFont.Font(family="Helvetica",size=36,weight="bold")

mycolor = '#%02x%02x%02x' % (64, 204, 208)

class OligoDatabase(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        container = tk.Frame(self, width=300, height=200, bg=mycolor)
        #not working bg color

        container.pack(side="top", fill="both", expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, OligosPage, ProjectsPage, ExperimentsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0,  sticky="NSEW")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        self.title("PathoFinder Oligo DB")#not the usual titlenaming
        frame = self.frames[cont]
        frame.tkraise() # raises the frame to the top

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)        

        
        label = tk.Label(self, text="Home")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Oligos", bg=mycolor,
                         command=lambda:controller.show_frame(OligosPage))
        button1.grid(row=2, column=2, pady=5, padx=10, sticky="WE")

        button2 = tk.Button(self, text="Projects",
                         command=lambda:controller.show_frame(ProjectsPage))
        button2.grid(row=4, column=2, pady=5, padx=10, sticky="WE")

        button3 = tk.Button(self, text="Employees")
                             # go to Employees page
        button3.grid(row=6, column=2, pady=5, padx=10, sticky="WE")

        button4 = tk.Button(self, text="Batches")
                            # go to batches page
        button4.grid(row=2, column=4, pady=5, padx=10, sticky="EW")

        button5 = tk.Button(self, text="Suppliers")
                            # go to Suppliers page
        button5.grid(row=4, column=4, pady=5, padx=10, sticky="EW")

        button6 = tk.Button(self, text="Experiments",
                        command=lambda:controller.show_frame(ExperimentsPage))
                            # go to Experiments page
        button6.grid(row=6, column=4, pady=5, padx=10, sticky="EW")

        button7 = tk.Button(self, text="Quit")
                            # Close the program
        button7.grid(row=8, column=8, pady=5, padx=10)

class OligosPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Oligo Menu")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame(StartPage))
        button1.grid(row=8, column=8, pady=5, padx=10)

        button2 = tk.Button(self, text="View All Oligos")
                            #goes to table view of all oligos
        button2.grid(row=4, column=2, pady=5, padx=10, sticky="WE")

        button3 = tk.Button(self, text="New Oligo")
                            #goes to new screen with textfields
        button3.grid(row=6, column=2, pady=5, padx=10, sticky="WE")

        button4 = tk.Button(self, text="Lookup Oligo")
                            #goes to table view of one oligo
        button4.grid(row=4, column=4, pady=5, padx=10, sticky="EW")

        button5 = tk.Button(self, text="Modify Oligo")
                            #gos to table view with textfields
        button5.grid(row=6, column=4, pady=5, padx=10, sticky="EW")

        
class ProjectsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Project menu")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame(StartPage))
        button1.grid(row=8, column=8, pady=5, padx=10)

class ExperimentsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Experiments menu")
        label.grid(columnspan=8, pady=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame(StartPage))
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
