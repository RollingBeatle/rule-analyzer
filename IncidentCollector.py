import argparse
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from urllib.parse import unquote



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--company', '-c', type=str, help='company to look for')
    parser.add_argument('--save', '-s', type=bool, help='save into csv')
    args = parser.parse_args()

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
            print("number of records "+str(len(data2)))
            counter = 0
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
                else:
                    print(f'error code {response.status_code}')
        
    

if __name__ == "__main__":
    main()
    