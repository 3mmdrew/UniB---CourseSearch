# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 16:51:46 2022
@author: Viola
"""

import webbrowser
import tkinter as tk
from PIL import ImageTk, Image
from functools import partial
from wallet import *
from searching import *

db = 'Bocconi.db'
courses_list = []

def runGUI():
    # Initialize homescreen
    struct = tk.Tk()
    struct.geometry("{0}x{1}+0+0".format(1200, 800))
    struct.title("Course Selection")

    #adding the background image
    try:
        bg = ImageTk.PhotoImage(Image.open("gui_req/Bocconi_resized.png"))
    except:
        image = Image.open('gui_req/Bocconi.jpg')
        new_image = image.resize((1200, 800))
        new_image.save('gui_req/Bocconi_resized.png')
        bg = ImageTk.PhotoImage(Image.open("gui_req/Bocconi_resized.png"))
    l = tk.Label(image=bg)
    l.pack()
    background = tk.Label(struct, width=50, height=25, bd=2, bg="white")
    background.place(relx=0.5, rely=0.475, anchor=tk.CENTER)

    #implementing the search screen
    header = tk.Label(struct, text="Welcome to your search engine for your course choice!", bg = "#FFFFFF",fg="black",
                      font=("Arial", 30, "bold"))
    header.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    text = tk.StringVar()
    label = tk.Label(struct, text="Enter here to search:", bg = "#FFFFFF", fg="black", font=("Arial", 20))
    label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    enter = tk.Entry(struct, font=("Arial", 10), textvar=text, width=30, bd=2, bg="white")
    enter.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
    creditselection = tk.Label(struct, text='Select credits', bg = "#FFFFFF", font=("Arial", 20))
    creditselection.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    maxCredits = tk.StringVar(struct)
    maxCredits.set("6")
    sp = tk.Spinbox(struct, from_=0, to=40, width=30, bd=2, textvariable=maxCredits)
    sp.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
    varUndergraduate = tk.IntVar()
    varGraduate = tk.IntVar()
    varArts = tk.IntVar()
    undergraduate = tk.Checkbutton(struct, variable=varUndergraduate, text="Undergraduate", bg = "#FFFFFF", padx=20)
    graduate = tk.Checkbutton(struct, variable=varGraduate, text="Graduate ", bg = "#FFFFFF", padx=20)
    masterOfArts = tk.Checkbutton(struct, variable=varArts, text="Integrated Master of Arts in Law ", bg = "#FFFFFF", padx=20)
    undergraduate.place(relx=0.462, rely=0.5, anchor=tk.CENTER)
    graduate.place(relx=0.55, rely=0.5, anchor=tk.CENTER)
    masterOfArts.place(relx=0.5, rely=0.53, anchor=tk.CENTER)

    # method for clicking on a button in order to handover to the result-view
    def searchButtonclicked():
        top = tk.Toplevel(struct)
        top.title("Search Results")
        top.geometry("{0}x{1}+0+0".format(1200, 800))
        top.grid()
        image = tk.Label(top, image=bg)
        image.pack()
        header = tk.Label(top, text="Your search results:", fg="black", bg = "#FFFFFF",
                          font=("Arial", 30, "bold"))
        header.place(x=600, y=80, anchor=tk.CENTER)
        search = enter.get()
        maxcredits = sp.get()
        if varUndergraduate.get() == 1 and varGraduate.get() == 0 and varArts.get() == 0:
            study_level = "UNDERGRADUATE"
        elif varUndergraduate.get() == 1 and varGraduate.get() == 1 and varArts.get() == 0:
            study_level = "UNDERGRADUATE,GRADUATE"
        elif varUndergraduate.get() == 1 and varGraduate.get() == 0 and varArts.get() == 1:
            study_level = "UNDERGRADUATE,INTEGRATED MASTER OF ARTS IN LAW"
        elif varUndergraduate.get() == 1 and varGraduate.get() == 1 and varArts.get() == 1:
            study_level = "UNDERGRADUATE,GRADUATE,INTEGRATED MASTER OF ARTS IN LAW"
        elif varGraduate.get() == 1 and varArts.get() == 1:
            study_level = "GRADUATE,INTEGRATED MASTER OF ARTS IN LAW"
        elif varGraduate.get() == 1 and varArts.get() == 0:
            study_level = "GRADUATE"
        elif varArts.get() == 1:
            study_level = "INTEGRATED MASTER OF ARTS IN LAW"
        else:
            study_level = "UNDERGRADUATE,GRADUATE,INTEGRATED MASTER OF ARTS IN LAW"

        #getting the outcome out of the search function
        outcome = best_output(db, search, maxcredits, study_level)
        del outcome[20:]
        frame_outcome = tk.Canvas(top, width=1050, height=300, bd=2, bg="white")
        frame = tk.Canvas(frame_outcome, width=1000, height=300, bd=2, bg="white")
        frame.grid(row=0, column=0, sticky='ns')

        # link a scrollbar to the result canvas
        vsb = tk.Scrollbar(frame_outcome, orient="vertical", command=frame.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        frame.configure(yscrollcommand=vsb.set)
        frame.propagate(0)

        #displaying the search results
        row = 1
        column = 0

        # method to change the view and see an overview of all of your courses in your wallet
        def addButtonclicked(i,list_in_use):
            itm = list_in_use[i]
            addToCart(itm,courses_list)

        #displaying every item in the result list to a table
        for item in outcome:
            resultList = item.split('; ')
            ind = outcome.index(item)
            for singleResult in resultList:
                if singleResult == "Sorry, there are no such subjects.":
                    result = tk.Label(frame, text="Sorry, there are no courses that match your preferences.",
                                      font=("Arial", 20, "bold"))
                    result.grid(row=row, column=column)
                    break
                else:
                    result = tk.Label(frame, text="Course ID", font=("Arial", 10, "bold"))
                    result.grid(row=0, column=0)

                    result = tk.Label(frame, text="Course name", font=("Arial", 10, "bold"))
                    result.grid(row=0, column=1)

                    result = tk.Label(frame, text="Link to Bocconi website", font=("Arial", 10, "bold"))
                    result.grid(row=0, column=2)

                    result = tk.Label(frame, text="Credits", font=("Arial", 10, "bold"))
                    result.grid(row=0, column=3)

                    result = tk.Label(frame, text="Add to wallet", font=("Arial", 10, "bold"))
                    result.grid(row=0, column=4)

                    if column == 2:
                        #button to open the website
                        link = tk.Button(frame, font=("Arial", 10, "bold"), text="Link to website", width=20,
                                         command=partial(webbrowser.open, singleResult))

                        link.grid(row=row, column=column)

                    else:
                        singleResult = (singleResult[:60] + '...') if len(singleResult) > 60 else singleResult
                        result = tk.Label(frame, text=singleResult, font=("Arial", 10, "bold"))
                        result.grid(row=row, column=column)

                    column += 1
            if resultList[0] == "Sorry, there are no such subjects.":
                break
            else:
                #add button, in order to put an item in your wallet
                add = tk.Button(frame, text="Add", font=("Arial", 10, "bold"), width=20, bd=2, command=partial(addButtonclicked,ind,outcome))
                add.grid(row=row, column=4)
            column = 0
            row += 1

        #display the frame with the results
        frame_outcome.config(scrollregion=frame_outcome.bbox("all"))
        frame_outcome.pack()
        frame_outcome.place(rely=0.55, relx=0.5, anchor=tk.CENTER)
    
    # calling Wallet Class
    def open_wallet(r,lst):
        Wallet_app(r,lst)

    #add the search button and a button to get to your wallet
    button = tk.Button(struct, text="Search", font=("Arial", 10, "bold"), width=30, bd=2, command=searchButtonclicked)
    button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    wallet_button = tk.Button(struct, text="Go to your wallet", font=("Arial", 10, "bold"), width=30, bd=2,
                       command=partial(open_wallet,struct,courses_list))
    wallet_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

    struct.mainloop()

# Adding information to wallet
def addToCart(to_add,crs):
    crs.append(to_add)


runGUI()