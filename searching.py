# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 13:28:45 2022

@author: Karolina

"""
import sqlite3
import re
import pandas as pd
import csv
import PDFscraping as pdf

def best_output(db, text, max_credits, study_level, pdf_version = False):
                 
    #preparing user input
    max_credits = int(max_credits)
    study_level = ''.join(study_level)
    study_level = study_level.split(',')
    user_input = text.lower() #changing letters to lowercase
    user_input = user_input.strip() #remove leading and trailing spaces
    user_input = re.sub(",","",user_input) #removing commas
    user_input = re.sub('[ \t\n]+', ' ', user_input) #remove all the tabs, new lines and multiple white spaces with single white space
    user_input = re.split('\s+', user_input) #spliting it to list of words
    
    #removing stopwords using list of words from nltk module -> list(stopwords.words('english'))
    stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 
                  'there', 'about', 'once', 'during', 'out', 'very', 'having', 
                  'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 
                  'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 
                  'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 
                  'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 
                  'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 
                  'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 
                  'ours','had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 
                  'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 
                  'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not',
                  'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 
                  'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 
                  'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was',
                  'here', 'than']
    user_list = []
    for w in user_input:
        if w not in stop_words:
            user_list.append(w)
        
    #connecting with db
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        if len(study_level) == 1:
            study_level = study_level[0] 
            c.execute(f'''select courseId, courseName, courseDescription 
                          from Courses 
                          where credits <= {max_credits} and credits > 0 and courseLevel = "{study_level}"''') ###course_id and description from db
        else:
            study_level = tuple(study_level)
            c.execute(f'''select courseId, courseName, courseDescription 
                          from Courses 
                          where credits <= {max_credits} and credits > 0 and courseLevel in {study_level}''')
        course_description = c.fetchall() #courseId, courseName and courseDescription
       
        ###dict = {course_id : coursename}
        prepared_dict_coursename = {} 
        for a in course_description:
            x = a[1]  
            x = x.lower()
            x = x.strip()
            x = x.strip(".")
            x = x.replace(".", '', 50)
            x = x.replace(":", '', 50)
            x = x.replace("!", '', 50)
            x = x.replace(",", '', 50)
            x = x.replace("?", '', 50)
            x = re.sub('[ \t\n]+', ' ', x) 
            x = re.sub(r'[()]', '', x)
            x = re.sub(r"[\[\]]",'', x)
            x = re.split('\s+', x)
            prepared_dict_coursename[a[0]] = x
        
        ###dict = {course_id : coursedescription}
        prepared_dict_coursedescription = {} 
        for a in course_description:
            x2 = a[2]
            x2 = x2.lower()
            x2 = x2.strip()
            x2 = x2.strip(".")
            x2 = x2.replace(".", '', 50)
            x2 = x2.replace(":", '', 50)
            x2 = x2.replace("!", '', 50)
            x2 = x2.replace(",", '', 50)
            x2 = x2.replace("?", '', 50)
            x2 = re.sub('[ \t\n]+', ' ', x2) 
            x2 = re.sub(r'[()]', '', x2)
            x2 = re.sub(r"[\[\]]",'', x2)
            x2 = re.split('\s+', x2)
            prepared_dict_coursedescription[a[0]] = x2
        
        #as a key course_id and as a value - how many words were found in a course name  
        occurances_coursename = {} 
        for course_id in prepared_dict_coursename:
            counter = 0
            for word in user_list:
                if word in prepared_dict_coursename[course_id]:
                    counter += 1
            occurances_coursename[course_id] = counter
        
        #as a key course_id and as a value - how many words were found in a course description 
        occurances_coursedescription = {} 
        for course_id in prepared_dict_coursedescription:
            counter = 0
            for word in user_list:
                if word in prepared_dict_coursedescription[course_id]:
                    counter += 1
            occurances_coursedescription[course_id] = counter
        
        #target: finding the maximum number of words that user is looking for
        lenght_of_user_list = len(user_list)
        
        #course_name
        ratio_for_coursename = {key: value / lenght_of_user_list for key, value in occurances_coursename.items()}
        df_coursename = pd.DataFrame.from_dict(ratio_for_coursename,  
                                               orient='index', 
                                               columns=['Occurances_CourseName'])
        
        #course_description
        ratio_for_coursedescription = {key: value / lenght_of_user_list for key, value in occurances_coursedescription.items()}
        df_coursedescription = pd.DataFrame.from_dict(ratio_for_coursedescription,  
                                                      orient='index', 
                                                      columns=['Occurances_Description'])
        
        #joining course name with course desciption on course_id
        df = df_coursename.merge(df_coursedescription, left_index=True, right_index=True)
        
        #calculating the ratio
        df['total_ratio'] = 0.7 * df['Occurances_CourseName'] + 0.3 * df['Occurances_Description']
        df = df[df['total_ratio'] >= 0.3]
        df = df.sort_values(by = 'total_ratio', ascending=False)
        
        #course_id in the correct order
        list_of_courseid = list(df.index.values)
        
        #selecting courses available for exchange students from csv file
        if pdf_version:
            pdf.readPdf()
            exchange_course_list = []
            with open("webs_req/codes.csv") as f:
                csv_reader = csv.reader(f, delimiter=",")
                for row in csv_reader:
                    if row[0] != "Code":
                        exchange_course_list.append(row[0])

        #selecting courses available for user that are ranked by ratio
        #output depends on pdf_version value, if it is for exchange students or for all students
        output_list = [] 
        if len(list_of_courseid) == 0:
            output_list =  ['Sorry, there are no such subjects.']
            return output_list
        else:
            for i in range(len(list_of_courseid)):
                final_output = list_of_courseid[i]
                if pdf_version:
                    if str(final_output) in exchange_course_list:
                        c.execute(f'''select courseId, courseName, courseURL, credits 
                                              from Courses 
                                              where courseId = {final_output}''')
                        response = c.fetchall()
                        output_list.append(response[0])
                else:
                    c.execute(f'''select courseId, courseName, courseURL, credits 
                                              from Courses 
                                              where courseId = {final_output}''')
                    response = c.fetchall()
                    output_list.append(response[0])
            
        #preparing the output -> list of strings ordered by ratio, separator ';'
        final_list = []
        for el in range(len(output_list)):
            list_course_id = list(output_list[el])
            new_string = '; '.join(str(e) for e in list_course_id)
            final_list.append(new_string)

        return final_list
