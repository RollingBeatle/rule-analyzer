import argparse
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from urllib.parse import unquote
import pandas as pd
import os
import PyPDF2

#Managed the dataFrame as a global variable
DataPd = None

#Clean save of the urls
def saveCSV(savedArr):
    df = pd.DataFrame(columns=['URL', 'visited'])
    df['URL'] = savedArr
    df['visited'] = 0
    df.to_csv('./results/incidentsURL.csv')
    global DataPd 
    DataPd = df

#Loading previous work
def readDownload():
    df = pd.read_csv("./results/incidentsURL.csv")
    global DataPd 
    DataPd = df
    missingPDF = df[df['visited'] == 0].values

    downloadNew(missingPDF)

#The actual downloading using an array of the links
def downloadNew(ReportLinks):

    counter = 0
    global DataPd
    for link in ReportLinks:
        delay = random.uniform(1,5)
        time.sleep(delay)
        pdf_url= link
        counter+=1
        response = requests.get(pdf_url)
        if response.status_code == 200:
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                # Split the header to find the filename part
                parts = content_disposition.split(';')
                for part in parts:
                    if 'filename' in part:
                        filename = part.split('=')[1].strip('" ')
                        break
                    else: 
                        filename = "unlabledReport"+str(counter)+'.pdf'
            else: 
                filename = "unlabledReport"+str(counter)+'.pdf'
            filename = unquote(filename)

            content = response.content
            with open(filename, "wb") as file:
                file.write(content)
            print('file saved')
            
            DataPd.at[counter,'visited'] = 1

        else:
            print(f'error code {response.status_code}')
    DataPd.to_csv('./results/incidentsURL.csv')
    
def PDFReading(pdfFile):
    pdf_file = open(pdfFile, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdf_file)
    pdfForm = pdfReader.get_fields()
    print(pdfForm)
    page = pdfReader.getPage(1)

    #print(page.items())

    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--company', '-c', type=str, help='company to look for')
    parser.add_argument('--save', '-s', type=bool, help='save into csv')
    parser.add_argument('--read', '-r', type=bool, help='Read pdf mode, this bypasses scrapping')
    
    args = parser.parse_args()
    if args.read:
        PDFReading("./results/pdfs/Apple_022123.pdf")
        return
    companyText = args.company
    driver = webdriver.Chrome()
    url = 'https://www.dmv.ca.gov/portal/vehicle-industry-services/autonomous-vehicles/autonomous-vehicle-collision-reports/'
    driver.get(url)
    data = driver.find_elements(By.CLASS_NAME, "accordion-block__header")
    print("the data is next")
    print(data)
    ReportLinks = []
    for i in data:
        try:
            i.click()
            data2 = driver.find_elements(By.PARTIAL_LINK_TEXT, companyText)
            for a in data2:
                print(a.text)
                print(a.get_attribute("href"))
                ReportLinks.append(a.get_attribute("href"))
        except Exception as e:
            break

    while True:
        companyText = str(input("New company to look for: \n"))
        if companyText == "exit":
            break
        for i in data:
            try:
                i.click()
                data2 = driver.find_elements(By.PARTIAL_LINK_TEXT, companyText)
                for a in data2:
                    print(a.text)
                    print(a.get_attribute("href"))
                    ReportLinks.append(a.get_attribute("href"))
            except Exception as e:
                break
    if args.save:
            if os.path.exists("./results/incidentsURL.csv"):
                option = str(input("file already exists, overwrite it? (Y/N) \n"))
                if option == 'Y':
                    saveCSV(ReportLinks)
                else: 
                    download = input("Continue downloading from file? (Y/N)")
                    if download == "Y":
                        readDownload()
                    else:    
                        return
            else:
                print("number of records "+str(len(ReportLinks)))
                saveCSV(ReportLinks)
                downloadNew(ReportLinks)

         
            
        
    

if __name__ == "__main__":
    main()
    