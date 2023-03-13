import requests
from bs4 import BeautifulSoup
from webs_req.DBManager import DBManager
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import tabula
import csv
from pdfrw import PdfReader, PdfWriter
import os

def readPdf():
    file = "webs_req/Course+offer+-+Fall+2022+-+ENG.pdf"
    output = "Course+offer+-+Fall+2022+-+ENG.pdf_noFirstPage"
    reader_input = PdfReader(file)
    writer_output = PdfWriter()
    for current_page in range(len(reader_input.pages)):
        if current_page > 0:
            writer_output.addpage(reader_input.pages[current_page])
    writer_output.write(output)

    tabula.convert_into(output, "courseOfferExchange.csv", output_format="csv", pages="all")
    list = []
    with open("courseOfferExchange.csv") as f:
        csv_reader = csv.reader(f, delimiter=",")
        for row in csv_reader:
            if row[0] != "" and row[0] != "Code1" and row[0] != "Code":
                list.append(row[0])
    df = pd.DataFrame(list, columns=["Code"])
    df.to_csv('webs_req/codes.csv', index=False)
    os.remove("courseOfferExchange.csv")
    os.remove("Course+offer+-+Fall+2022+-+ENG.pdf_noFirstPage")

def initializeDatabase():
    dbManager = DBManager("Bocconi.db")
    dbManager.createTable("Courses", '''(courseId INT, courseName TEXT, courseURL TEXT, courseDescription TEXT, credits INT,
    courseLevel TEXT, PRIMARY KEY('courseId'))''')
    dbManager.close()

def courseList():
    dbManager = DBManager("Bocconi.db")

    URL = "https://didattica.unibocconi.eu/ts/tsn_ric_num.php?anno=2023&IdPag=6896&ts_arg_cod=&ts_arg_des=&cerca=search"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "lxml")
    elements = soup.find_all("tr")
    result = set()
    links = set()
    for e in elements:
        link = e.find_next("a", class_="bold")
        courseURL = "https://didattica.unibocconi.eu/ts/" + link.get("href")
        courseId = link.text.strip()
        title = link.find_next("td", style="border-bottom: 1px solid #cccccc; vertical-align:top;")
        courseName = title.text.strip()
        courseLevel = ""
        if (courseId[0]).__eq__("3"):
            courseLevel = "UNDERGRADUATE"
        if (courseId[0]).__eq__("2"):
            courseLevel = "GRADUATE"
        if (courseId[0]).__eq__("5"):
            courseLevel = "INTEGRATED MASTER OF ARTS IN LAW"
        courseId = int(courseId)
        result.add((courseId, courseName, courseURL, "", 0, courseLevel))
        links.add(courseURL)

    convertedresult = list(result)
    dbManager.insertRow("Courses",
                        "(courseId, courseName, courseURL, courseDescription, credits, courseLevel) VALUES (?, ?, ?, ?, ?, ?)",
                        convertedresult)
    dbManager.close()
    return list(links)


def getDescription(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    title = soup.find("div", class_="tit_blue", string="CONTENT SUMMARY")
    if title is None:
        title = soup.find("div", class_="tit_blue", string="PROGRAMMA SINTETICO")
    if title is None:
        title = soup.find("div", class_="tit_blue", string="PROGRAMMA SINTETICO / CONTENT SUMMARY")
    if title is None:
        return
    description = title.find_next("div").text.strip()
    description = description.replace("\'", "")
    description = description.replace('\"', "")
    dbManager = DBManager("Bocconi.db")
    dbManager.updateRow("Courses", f"courseDescription = '{description}'", f"courseURL = '{url}'")
    dbManager.close()


def getCredits(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    title = soup.find("div", style="background-color: #0c5299; font-size: 16px; padding:10px; color: #fff; "
                                   "font-family: "
                                   "Georgia, 'Times New Roman', Sans-Serif;")
    text = title.text.strip()
    positionOfCredits = text.find("credits")
    try:
        result = int(text[positionOfCredits - 2])
        if text[positionOfCredits - 3].__eq__("1"):
            result += 10
    except:
        result = 0
    dbManager = DBManager("Bocconi.db")
    dbManager.updateRow("Courses", f"credits = {result}", f"courseURL = '{url}'")
    dbManager.close()


def main():
    initializeDatabase()
    urls = courseList()
    with ThreadPoolExecutor() as p:
        p.map(getDescription, urls)
        p.map(getCredits, urls)


if __name__ == '__main__':
    # main()
    print(readPdf())
