#importing required dependencies
import tkinter as tk
from functools import partial

def credit_total(c): #function to get sum of credits from string inputs
    tot = 0
    for s in c:
        try:
            tot += int(s[-1])
        except:
            return 'error'
    return tot

def structure_course_list(c):
    new = []
    for rsl in c:
        n_rsl = list(rsl.split('; '))
        name = n_rsl[1]
        if len(name) > 34: 
            name = name[:34] + '...'
        fin = n_rsl[0]+', '+name+', '+ n_rsl[3]
        new.append(fin)
    return new

def clipboard_list(c):
    new = []
    for rsl in c:
        n_rsl = list(rsl.split('; '))
        fin = n_rsl[0]+', '+rsl[1]+', '+ n_rsl[3]
        new.append(fin)
    return new

wallet_courses = []

class Wallet_app:
    def __init__(self, tplevel, i_courses=[]):
        self.i_courses = i_courses
        #define main variables of interest
        self.clipboard = clipboard_list(i_courses) #normal class output
        self.courses = structure_course_list(i_courses) #class data to present 
        self.credits = credit_total(self.courses)
        root = tk.Toplevel(tplevel)

        self.root = root

        #setting title
        root.title("Wallet")

        #setting window size
        width=600
        height=280
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)

        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.iconbitmap("wallet_req/w_icon.ico")

        #base labels and buttons - repeated ones are looped in for loop
        for c in self.courses:
            ind = self.courses.index(c)
            hy = 40 + ((ind)*30)
            class_profile=tk.Label(root,text=c,justify="center",fg="#333333",font=('Times',10))
            class_profile.place(x=20,y=hy,width=335,height=30)

            del_button=tk.Button(root,bg="#e9e9ed",font=("Times",10),fg="#000000",justify="center",text="Delete",command=partial(self.deletecomm,ind))
            del_button.place(x=400,y=hy,width=70,height=25)

        ref_button=tk.Button(root,bg="#e9e9ed",font=("Times",10),fg="#1e90ff",justify="center",text="Refresh",command=self.refreshcomm)
        ref_button.place(x=510,y=10,width=70,height=25)

        totcredits=tk.Label(root,text="Total Credits = %d" % self.credits,justify="center",fg="#333333",font=('Times',10))
        totcredits.place(x=50,y=10,width=174,height=30)

    def deletecomm(self,i): #function gathering row to delete
        self.i_courses.pop(i) #take item out of list of courses

    def refreshcomm(self): #refresh window by stripping and re-initialising
        upd = self.i_courses
        for ele in self.root.winfo_children(): #strip window of all elements
            ele.destroy()
        self.root.withdraw()
        Wallet_app(self.root,upd) #re-initialise

''' Redundant as pyperclip is not a standard python library

    exp_button=tk.Button(root,bg="#e9e9ed",font=("Times",10),fg="#000000",justify="center",text="Copy to Clipboard",command=self.exportcomm)
    exp_button.place(x=475,y=240,width=110,height=25)

    def exportcomm(self): #export list to the clipboard using pyperclip module
        txt = ''
        for i in self.clipboard:
            txt = txt + i + ';\n'
        pyperclip.copy(txt)
'''
