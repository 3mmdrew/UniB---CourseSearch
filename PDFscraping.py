# DISCLAIMER: as said in the documentation this is not the core part of the project and doesn't contribute to the main
# functionality. If you still want to execute this, the importing instructions are in the documentation.
import pandas as pd
import tabula
import csv
from pdfrw import PdfReader, PdfWriter
import os

# scrape the pdf and create a csv file with only courseIds as an output ("Codes.csv"). This can then be compared in the
# searching class with the "Bocconi.db" database to create the intersection.
def readPdf():
    file = "webs_req/Course+offer+-+Fall+2022+-+ENG.pdf"

    # create a new pdf without the first page, as it doesn't contain a table and therefore can't be read by tabula
    output = "Course+offer+-+Fall+2022+-+ENG.pdf_noFirstPage"
    reader_input = PdfReader(file)
    writer_output = PdfWriter()
    for current_page in range(len(reader_input.pages)):
        if current_page > 0:
            writer_output.addpage(reader_input.pages[current_page])
    writer_output.write(output)

    # convert the pdf without first page into a csv file (""courseOfferExchange.csv")
    tabula.convert_into(output, "courseOfferExchange.csv", output_format="csv", pages="all")

    # problem: the scraped csv file has many null values and blank lines. Therefore we will create a new csv ("Codes.csv")
    # with only the ids which will suffice for comparing it to the database.
    list = []
    with open("courseOfferExchange.csv") as f:
        csv_reader = csv.reader(f, delimiter=",")
        for row in csv_reader:
            if row[0] != "" and row[0] != "Code1" and row[0] != "Code":
                list.append(row[0])
    df = pd.DataFrame(list, columns=["Code"])
    df.to_csv('webs_req/Codes.csv', index=False)

    # delete the files that we created in the run time to keep the directory clean
    os.remove("courseOfferExchange.csv")
    os.remove("Course+offer+-+Fall+2022+-+ENG.pdf_noFirstPage")