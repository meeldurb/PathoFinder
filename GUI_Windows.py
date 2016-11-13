"""Author: Melanie van den Bosch
Jorn van der Ent
Script for having multiple windows frames in a GUI"""

from __future__ import division
import math 
import Tkinter as tk

class OligoDatabase(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, OligosPage, ProjectsPage, ExperimentsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #self.master.title("PathoFinder Oligo DB")
        
        label = tk.Label(self, text="Home")
        label.grid(pady=10, padx=10)

        button1 = tk.Button(self, text="Oligos",
                         command=lambda:controller.show_frame(OligosPage))
        button1.grid()

        button2 = tk.Button(self, text="Projects",
                         command=lambda:controller.show_frame(ProjectsPage))
        button2.grid()

        button3 = tk.Button(self, text="Employees")
                             # go to Employees page
        button3.grid()

        button4 = tk.Button(self, text="Batches")
                            # go to batches page
        button4.grid()

        button5 = tk.Button(self, text="Suppliers")
                            # go to Suppliers page
        button5.grid()

        button6 = tk.Button(self, text="Experiments",
                        command=lambda:controller.show_frame(ExperimentsPage))
                            # go to Experiments page
        button6.grid()

class OligosPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Oligo Menu")
        label.grid(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame(StartPage))
        button1.grid()

        button2 = tk.Button(self, text="View All Oligos")
                            #goes to table view of all oligos
        button2.grid()

        button3 = tk.Button(self, text="New Oligo")
                            #goes to new screen with textfields
        button3.grid()

        button4 = tk.Button(self, text="Lookup Oligo")
                            #goes to table view of one oligo
        button4.grid()

        button5 = tk.Button(self, text="Modify Oligo")
                            #gos to table view with textfields
        button5.grid()

        
class ProjectsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Project menu")
        label.grid(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame(StartPage))
        button1.grid()

class ExperimentsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Experiments menu")
        label.grid(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                         command=lambda:controller.show_frame(StartPage))
        button1.grid()

        button2 = tk.Button(self, text="View All Experiments")
                             #show a table view of all experiments
        button2.grid()

        button3 = tk.Button(self, text="New Experiment")
                             #show some text fields for adding experiments
        button3.grid()

        button4 = tk.Button(self, text="Edit Experiments")
                             #show text fields where you can browse for experiment
        button4.grid()

        button5 = tk.Button(self, text="Lookup")
                             #show text fields where you can lookup
        button5.grid()


if __name__ == "__main__":
    app = OligoDatabase()
    app.mainloop()
