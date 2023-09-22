import argparse
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument('--word', '-w', type=str, help='word to look into')
    parser.add_argument('--save', '-s', type=bool, help='save into csv')
    args = parser.parse_args()

    driver = webdriver.Chrome()
    url = 'https://www.dmv.ca.gov/portal/vehicle-industry-services/autonomous-vehicles/autonomous-vehicle-collision-reports/'
    driver.get(url)
    data = driver.find_elements(By.CLASS_NAME, "accordion-block__header")
    print("the data is next")
    print(data)
    
    for i in data:
        try:
            i.click()
            data2 = driver.find_elements(By.PARTIAL_LINK_TEXT, "Cruise")
            for a in data2:
                print(a.text)
                print(a.get_attribute("href"))
        except Exception as e:
            break
    

if __name__ == "__main__":
    main()
    