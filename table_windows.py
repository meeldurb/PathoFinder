from Tkinter import *
from tkFont import Font
from math import floor
import config as cfg
import Table_Lookup_queries as TLQ
import re
import tkFont

mycolor = '#%02x%02x%02x' % (0, 182, 195)

class Spreadsheet(Frame):

    def __init__(self, parent, font=None, **keywords):
        Frame.__init__(self, parent)
        self.columns=[]

        
        # Setup font information
        if font:
            self.txtFont=font
        else:
            self.txtFont=Font(family="Arial", size=14)
        self.defaultRowHeight=self.txtFont['size']+7

        self.headerFont=self.txtFont.copy()
        self.headerFont.configure(weight='bold')

        self.spreadsheet=Canvas(self, bg='white', bd=0,
                                highlightthickness=0, **keywords)
        self.header=Canvas(self, height=self.defaultRowHeight+2, bd=0,
                                highlightthickness=0, bg='white')
        self.header.pack(side=TOP, expand=FALSE, fill=X, pady=0)

        self.scrollY = Scrollbar(self, orient=VERTICAL,
                                command=self.spreadsheet.yview )
        self.scrollX = Scrollbar(self, orient=HORIZONTAL, command=self.xview )
        self.spreadsheet["xscrollcommand"] = self.scrollX.set
        self.spreadsheet["yscrollcommand"] = self.scrollY.set
        self.scrollY.pack(side="right", fill="y")
        self.scrollX.pack(side="bottom", fill="x")
        self.spreadsheet.pack(fill="both", expand=True, side="left")

        # Set up the mousewheel to scroll
        self.spreadsheet.focus_set()
        self.spreadsheet.bind("<MouseWheel>", self.mouseScroll)

        # Store current cursor (the one to restore to after a change)
        self.defaultCursor=self.cget("cursor")

        self.bind("<Configure>", self.catchResize)


    def catchResize(self, event):
        try:
            self.after_cancel(self.config_id)
        except: pass
        self.config_id = self.after(500, self.optimiseColumns)


    def xview(self, *args):
        self.header.xview(*args)
        self.spreadsheet.xview(*args)

    def initialise(self):

        self.spreadsheet.delete(ALL)

        # Any window items still bound, destroy
        for c in self.spreadsheet.children.values(): c.destroy()

        self.columns=[]
        self.rows=[]
        self.startCol=0
        self.startRow=0
        self.totalHeight=0


    def mouseScroll(self, event):
        if event.delta >0:
            self.spreadsheet.yview("scroll", "-1", "units")
        else:
            self.spreadsheet.yview("scroll", "1", "units")


    def setupColumns(self, columns):

        self.columns=[]

        for i in range(0, len(columns)):
            column=columns[i]
            name=column[0]
            width=column[1]
            if len(column)>2:
                align=column[2]
            else:
                align=CENTER
            self.columns.append([name,width,align])


    def addColumn(self, label, width=50, align=LEFT, bg='white', fg='black'):
        col=dict()
        col['label']=label
        col['width']=width
        col['align']=align
        col['bg']=bg
        col['fg']=fg
        self.columns.append(col)

    def addRow(self, pos, row):
        row=Row(row)
        row.height=self.getRowHeight(row)

        row.widgets=[]
        col=0
        for item in row:
            colDat=self.columns[col]
            if isinstance(item, Widget):
                row.widgets.append(item)
                item.internal=False
            else:
                if item == 'delivered' or item == 'approved':
                   e=Listbox(self.spreadsheet, bg= 'green',
                        fg=colDat['fg'], font=self.txtFont)
                elif item == 'ordered' or item == 'neutral':
                    e=Listbox(self.spreadsheet, bg='yellow',
                        fg=colDat['fg'], font=self.txtFont)
                elif item == 'processed':
                    e=Listbox(self.spreadsheet, bg='orange',
                        fg=colDat['fg'], font=self.txtFont)
                elif item == 'out of stock' or item == 'disapproved':
                    e=Listbox(self.spreadsheet, bg='red',
                        fg=colDat['fg'], font=self.txtFont)
                else:
                    e=Listbox(self.spreadsheet, bg=colDat['bg'],
                        fg=colDat['fg'], font=self.txtFont)
                e.internal=True
                e.insert(END, item)
                if colDat['align']==RIGHT: e.xview(END)

                row.widgets.append(e)
            col += 1

        if pos==END:
            self.rows.append(row)
        else:
            self.rows.insert(pos, row)

    def getRowHeight(self, row):
        maxh=0
        for item in row:
            maxh=max(maxh, self.valHeight(item))
        return maxh


    def optimiseColumns(self, fixedWidth = True):
        if not self.columns: return

        # 1. Find the current total
        totWidth=0
        for column in self.columns:
            totWidth+=column['width']

        # Minimise columns which can be
        newWidth=0
        for col in range(0, len(self.columns)):
            maxwidth=self.neededWidth(col)
            colObj=self.columns[col]
            if maxwidth<colObj['width']:
                colObj['width']=maxwidth
            newWidth+=colObj['width']

        # Now, if some columns need more space, and it is available, give it to them
        swidth=self.spreadsheet.winfo_width()
        if swidth<2:
            swidth=self.spreadsheet.winfo_reqwidth()

        if swidth>newWidth:
            # we have free space

            expand=[]
            for col in range(0, len(self.columns)):
                coldat=self.columns[col]
                reqwidth=self.neededWidth(col)
                if reqwidth>coldat['width']:
                    expand.append((coldat, reqwidth-coldat['width']))

            # Now, we assign each col an equal share of the free space,
            # up to their max requirement
            free=swidth-newWidth
            expand.sort(cmp=lambda a, b: cmp(a[1], b[1]))
            while expand:
                if free<1: break
                col,req=expand.pop()
                req=min(free, req)
                col['width']+=req
                free=free-req

        self.show()

    def neededWidth(self, col):
        maxwidth=self.headerFont.measure(self.columns[col]['label'])
        for row in self.rows:
            wdth=self.valWidth(row[col])
            maxwidth=max(wdth, maxwidth)
        return maxwidth+6


    def valWidth(self, val):
        if isinstance(val, basestring):
            return self.txtFont.measure(val)
        try:
            return val.winfo_reqwidth()
        except: pass


    def valHeight(self, val):
        if isinstance(val, basestring):
            return self.defaultRowHeight
        try:
            return val.winfo_reqheight()
        except: pass


    ##########################################
    # REDRAWING

    # REDRAW after change of screensize
    # Called after screen resize or the first time

    def show(self):
        self.spreadsheet.delete(ALL)
        self.redrawHeader()
        self.redrawSheet()

    def redrawHeader(self):
        self.header.delete(ALL)
        x=5
        height=self.defaultRowHeight+2
        self.header.create_line(x, 2, x, height)
        count=0
        for col in self.columns:
            width=col['width']
            self.header.create_rectangle(x+1, 3, x+width-1, height-1,
                                        fill="#c1c2ef", outline="#c1c2ef")
            self.header.create_line(x, 2, x+width, 2)
            self.header.create_line(x, height, x+width, height)
            self.header.create_line(x+width, 2, x+width, height,
                                    tags=('colend', str(count)))

            self.header.create_text(x+width/2, 1, text=col['label'],
                                    anchor=N, font=self.headerFont, tags=('title', str(count)))
            # for the endline use a rect of width 3, but the border same as background
            # Basically, this gives us a widget of 3 pix width for detecting enter/leave events
            self.header.create_rectangle(x+width-1, 2, x+width+1,
                                        height, fill='black', outline="#c1c2ef", tags=('colend', str(count)))
            x+=width
            count+=1

        self.header["scrollregion"]=(0,0, x+self.scrollY.winfo_reqwidth(), height)

        # Make sure all controls are on top
        self.header.tag_raise('colend')
        self.header.tag_bind("colend", "<Enter>", self.enterColEnd)
        self.header.tag_bind("colend", "<Leave>", self.leaveColEnd)
        self.header.tag_bind("colend", "<Button-1>", self.startDrag)
        self.header.tag_bind("title", "<ButtonRelease>", self.orderByColumn)

    def redrawSheet(self):
        if not self.rows: return
        # now show the data
        y=0
        for row in self.rows:
            height=row.height
            x=5
            col=-1
            for value in row.widgets:
                col+=1
                width=self.columns[col]['width']
                self.drawCell(x, y, width, height, value, self.columns[col])
                x+=width
            y+=height

        self.spreadsheet["scrollregion"]=(0,0, x, y)

    def orderByColumn(self, event):
        wgt=self.header.find_withtag('current')
        colID=int(self.header.gettags(wgt)[1])
        self.sortOnColumn(colID)

    def enterColEnd(self, event):
        self.header.configure(cursor='sb_h_double_arrow')

    def leaveColEnd(self, event):
        self.header.configure(cursor=self.defaultCursor)

    def startDrag(self, event):
        self.wgt1=self.header.find_withtag('current')
        self.currCol=self.columns[int(self.header.gettags(self.wgt1)[1])]
        self.startX=self.header.bbox(self.wgt1)[0]
        self.header.bind('<B1-Motion>', self.moveBorder)
        self.header.bind('<ButtonRelease>', self.stopMoveBorder)

    def moveBorder(self, event):
        self.header.tag_raise(self.wgt1)
        wgt_x=self.header.bbox(self.wgt1)[0]
        diff=event.x-wgt_x
        self.header.move(self.wgt1, diff, 0)

    def stopMoveBorder(self, event):
        self.header.unbind('<B1-Motion>')
        self.header.unbind('<ButtonRelease>')
        self.grab_release()
        wgt_x=self.header.bbox(self.wgt1)[0]
        change=wgt_x-self.startX
        self.currCol['width']+=change
        self.show()

    def drawCell(self, x, y, width, height, value, col):
        if value.internal:
            self.spreadsheet.create_window(x, y,  window=value,
                                        height=height, width=width, anchor=NW)
        else:
            wheight=min(height-2,value.winfo_reqheight())
            self.spreadsheet.create_window(x+width/2, y+height/2,
                                        window=value, height=wheight, anchor=CENTER)

    def sortOnColumn(self, colID):
        self.rows.sort(cmp=lambda a, b, c=colID: cmp(a[c], b[c]))
        self.show()

class Row(list):

    def __init__(self, vals):
        if isinstance(vals, tuple): vals=list(vals)
        list.__init__(self, vals)
        self.height=0

class ButtonsFrame(Frame):
    def __init__(self, parent, sql, table_str, attributes, sortattribute, sortmethod):
        Frame.__init__(self, parent)
        
        # set font
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(family="Corbel", size=24)
        self.tk_setPalette(background=mycolor, foreground="white",
                           activeBackground="grey", activeForeground="black")

        self.master.title(table_str)

        # set frame in oder to be able to refresh
        self.frame = parent

        # set variables
        self.sortattribute = StringVar()
        self.sortattribute.set(sortattribute)
        self.sortmethod = StringVar()
        self.sortmethod.set(sortmethod)
        self.search_input = StringVar()

        # Set Buttons
        refreshButton = Button(parent, text="Refresh", width = 8)
        refreshButton['command'] = lambda : self.refresh(sql, table_str, attributes, self.sortattribute.get(), self.sortmethod.get())
        refreshButton.pack(side=LEFT, pady = 5, padx = 10)

        searchButton = Button(parent, text="Search", width = 8)
        searchButton['command'] = lambda : self.open_search_window(table_str, attributes, self.sortattribute.get(), self.sortmethod.get())
        searchButton.pack(side=LEFT, pady = 5, padx = 10)
        
        quitButton = Button(parent, text="Quit", width = 8)
        quitButton['command'] = lambda : parent.destroy()
        quitButton.pack(side=RIGHT, pady = 5, padx = 10)

        # Setup a Frame which contains all the sort widgets
        sort_group = LabelFrame(parent, relief = 'flat')
        sort_group.pack(padx=10)
        
        sortList = OptionMenu(sort_group, self.sortattribute, *attributes)
        sortList['width'] = 20
        sortList['height'] = 1
        sortList.pack(side=LEFT, pady = 5, padx = 10)

        sortmethodList = OptionMenu(sort_group, self.sortmethod,'Ascending', 'Descending')
        sortmethodList['width'] = 20
        sortmethodList['height'] = 1
        sortmethodList.pack(side=LEFT, pady = 5, padx = 10)

        sortbutton = Button(sort_group, text = 'Sort', width = 8)
        sortbutton['command'] = lambda : self.sort_table(sql, table_str, attributes, self.sortattribute.get(), self.sortmethod.get())
        sortbutton.pack(side = RIGHT, pady = 5, padx = 10)

    def open_search_window(self, table_str, attributes, sortattribute, sortmethod):
        win = Toplevel()
        
        label1 = Label(win, text = 'Search')
        label1.pack(side = 'top', pady = 20)
        
        # Search Group
        search_group = LabelFrame(win, relief = 'flat')
        search_group.pack(side = 'top', pady = 5, padx = 10)
        
        search_label = Label(search_group, text = 'Search for: ')
        search_label.pack(side = 'left', pady = 5, padx = 10)

        search_entry = Entry(search_group, width = 50)
        search_entry['textvariable'] = self.search_input
        search_entry.pack(side = 'left', pady = 5, padx = 10)


        label2 = Label(win, text = 'Sort By:')
        label2.pack(side = 'top', pady = 20)
        
        # Sort Group
        sort_group = LabelFrame(win, relief = 'flat')
        sort_group.pack(side = 'top')
        
        sortList = OptionMenu(sort_group, self.sortattribute, *attributes)
        sortList.pack(side=LEFT, pady = 5, padx = 10)

        sortmethodList = OptionMenu(sort_group, self.sortmethod, 'Ascending', 'Descending')
        sortmethodList.pack(side=LEFT, pady = 5, padx = 10)


        # Action Buttons
        action_group = LabelFrame(win, padx = 50, relief = 'flat')
        action_group.pack(side = 'top', pady = 20)

        # Go
        sortbutton = Button(action_group, text = 'GO', width = 10)
        sortbutton['command'] = lambda : self.search_button_go(table_str, self.search_input.get(), self.sortattribute.get(), self.sortmethod.get(), win)
        sortbutton.pack(side = 'left' , pady = 5, padx = 10)

        # Cancel
        cancelbutton = Button(action_group, text = 'Cancel', width = 10)
        cancelbutton['command'] = lambda : win.destroy()
        cancelbutton.pack(side = 'right', pady = 5, padx = 10)

    def search_button_go(self, table_str, search_input, sortattribute, sortmethod, window):
        sql, attributes = TLQ.search(table_str, search_input, sortattribute, sortmethod)
        window.destroy()
        self.refresh(sql, table_str, attributes, sortattribute, sortmethod)
        
 

    def refresh(self, sql, table_str, attributes, sortattribute, sortmethod):
        """Destroy the window in order to build a new one

        Keyword Arguments:
        sql             -- string, SQL query statement including an ORDER BY
        attributes      -- list, list of all the attributes of the current table
        sortattribute   -- string, an attribute of the current table
        sortmethod      -- string, either Ascending or Descending"""
        if self.frame is not None:
            self.frame.destroy()
        # build new one
        self.frame = TLQ.build_table_window(sql, table_str, attributes, sortattribute, sortmethod)

    def sort_table(self, sql, table_str, attributes, sortattribute, sortmethod):
        """Destroy the window in order to build a new one

        Keyword Arguments:
        sql             -- string, SQL query statement including an ORDER BY
        attributes      -- list, list of all the attributes of the current table
        sortattribute   -- string, an attribute of the current table
        sortmethod      -- string, either Ascending or Descending"""
        
        # check for valid sortmethod
        if sortmethod != 'Ascending' and sortmethod != 'Descending':
            raise ValueError("Sortmethod should be Ascending or Descending")
        # check for valid attribute
        if sortattribute not in attributes:
            raise ValueError("Selected attribute does not occur in this table")

        # make the right sortmethod syntax
        if sortmethod == 'Ascending':
            sortmethod_syntax = 'ASC'
        else:
            sortmethod_syntax = 'DESC'

        # build pattern finder
        pattern = r'(ORDER BY )[^ \t\n\r\f\v]*( )[A-Z]*'
        matcher = re.compile(pattern)
        sub = r'\1%s\2%s' % (sortattribute, sortmethod_syntax)
        # replace text in the query
        sql = matcher.sub(sub, sql)

        # refresh the window with the new settings
        self.refresh(sql, table_str, attributes, sortattribute, sortmethod)


