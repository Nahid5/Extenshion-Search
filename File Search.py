"""
Creator: Nahid Sarker
This scans selected file location for files with the indicated extenshion
"""
import tkinter as tk
from tkinter import *
import tkinter.messagebox
import glob, os
from collections import Counter

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       encod = 'utf-8'

       # ------------------------Text boxes-----------------------
       # are on grids and the text are allighed on the west side
       # ext, and dir are where the entry is stored
       ext = StringVar()
       dir = StringVar()
       Label(self, text="Enter desired extenshion: ").grid(row=0, column=0, sticky=W)
       Entry(self, textvariable=ext).grid(row=0, column=1)
       Label(self, text="Enter desired directory: ").grid(row=1, column=0, sticky=W)
       Entry(self, textvariable=dir).grid(row=1, column=1)

       # -----------------------Check Box---------------------------
       yesNo = IntVar()  # 1 for checked, 0 for not
       Checkbutton(self, text="Unchecked for single directory, and checked for all subbdirectories",
                                       variable=yesNo).grid(row=2, column=0)

       ext.set(".your file extenshion")
       dir.set(r"\file location in the drive")

       # ----------------------The function that does everything----------------------
       def doTheSearch():
           # w truncates existing file. docs: Modes 'r+', 'w+' and 'a+' open the file for updating (note that 'w+' truncates the file).
           nameOfOutput = "Output.txt"
           output = open(nameOfOutput, 'w', encoding=encod)

           if (yesNo.get() == 0):  # searches just the input directory
               for file in os.listdir(dir.get()):  # need to use .get before the entry variables to get the values
                   if file.endswith(ext.get()):
                       output.write(dir.get() + file + '\n')

           else:
               for self, dirs, files in os.walk(
                       dir.get()):  # searches the input and all subdirectories in the input directory
                   for file in files:
                       if file.endswith(ext.get()):
                           output.write(os.path.join(self, file) + '\n')  # prints results to a txt file named Output

           output.close()
           output = open(nameOfOutput, 'r', encoding=encod)
           lines = []
           extNames = "OutputNames.txt"
           outputExtnames = open(extNames, 'w+', encoding=encod)

           for line in output:  # appends each line of the file into a list
               lines.append(line)

           for x in range(len(lines)):
               sentance = lines[x]  # line x is stored in sentance
               y = 1  # y = 1 so not out of bounds
               while sentance[len(sentance) - y] != "\\":  # starting from the end until \ is reached
                   y += 1
               y -= 1  # so \ is not included in the name
               outputExtnames.write(sentance[-y:])  # copies from y to the end of the sentance

           outputExtnames.close()
           output.close()

       # ----------------------Submit Button------------------------
       Button(self, text="Submit", command=doTheSearch).grid(row=3, column=3)

"""
The location of the files found
"""
class Page2(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       scrollbar = Scrollbar(self)
       scrollbar.pack(side=RIGHT, fill=Y)
       mylist = Listbox(self, yscrollcommand=scrollbar.set)
       def refresh():
           mylist.delete(0,END)     #deletes so old data is gone
           file = open("Output.txt", 'r', encoding='utf-8')
           for line in file:
               mylist.insert(END, str(line))
           mylist.pack(side=LEFT, fill=BOTH, expand=True)
           scrollbar.config(command=mylist.yview)
           file.close()

       Button(self, text="Refresh", command = refresh).pack(side = TOP)


"""
The names of the files found
"""
class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

       scrollbar = Scrollbar(self)
       scrollbar.pack(side=RIGHT, fill=Y)
       mylist = Listbox(self, yscrollcommand=scrollbar.set)
       def refresh():
           mylist.delete(0, END)        #deletes so old data is gone
           file = open("OutputNames.txt", 'r', encoding='utf-8')
           for line in file:
               mylist.insert(END, str(line))
           mylist.pack(side=LEFT, fill=BOTH, expand=True)
           scrollbar.config(command=mylist.yview)
           file.close()

       Button(self, text="Refresh", command=refresh).pack(side=TOP)

class Page4(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       scrollbar = Scrollbar(self, orient=HORIZONTAL)
       scrollbar.pack(side=BOTTOM, fill=X)
       mylist = Listbox(self, xscrollcommand=scrollbar.set)

       def refresh():
           mylist.delete(0, END)  # deletes so old data is gone
           with open("OutputNames.txt", 'r', encoding='utf-8') as f:
               content = f.readlines()
               lists = content

           lists = list(map(str.strip, lists))  # to remove \n
           mylist.insert(END, Counter(lists))
           mylist.pack(side=LEFT, fill=BOTH, expand=True)
           scrollbar.config(command=mylist.xview)

           f.close()

       Button(self, text="Refresh", command=refresh).pack(side=TOP)


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Search Page", command=p1.lift)
        b2 = tk.Button(buttonframe, text="File Location", command=p2.lift)
        b3 = tk.Button(buttonframe, text="File Name", command=p3.lift)
        b4 = tk.Button(buttonframe, text="Occurance", command=p4.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")

        p1.show()

        def aboutText():
            tkinter.messagebox.showinfo(
                message="Created by Nahid Sarker\nThis Program finds all files with the same extenshion.")
        # ------------------Main Menu-----------------
        topMenu = Menu(root)
        root.config (menu=topMenu)  # config polaces the menu at top
        subMenu = Menu(topMenu)
        topMenu.add_cascade(label="File", menu=subMenu)
        subMenu.add_command(label="Exit", command=exit)

        aboutMenu = Menu(root)
        topMenu.add_cascade(label="About", menu = aboutMenu)
        aboutMenu.add_command(label="About author and program", command=aboutText)

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    root.title("Extension finder")
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x400")

    root.mainloop()