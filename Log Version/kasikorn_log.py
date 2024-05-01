from bs4 import BeautifulSoup 
import requests 
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
#Fix
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import re 
import pandas as pd 
import schedule
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import logging


    
# ชื่อไฟล์
filename = f'scrape_kasikorn_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
log_file = f'logging_kasikorn_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'



# option headless
options = Options()
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

start = 1 
end = 2  # end page 


main_url = "https://www.kasikornbank.com/th/propertyforsale/search/pages/index.aspx?&CurrentPageIndex=4&Ordering=Hot&Tab=newProperty"
driver.get(main_url)

for page in range(start,end+1): 
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(3)
    elem = driver.find_element(By.CSS_SELECTOR,'a.load-more-btn')
    elem.click()

# url link
lis = [ i.get_attribute('href') for i in driver.find_elements(By.CSS_SELECTOR,'a.result-img')]



img_lis = [ i.get_attribute('src') for i in driver.find_elements(By.CSS_SELECTOR,'a.result-img > img')]
print(img_lis,len(img_lis))



area_lis = [ i.text.replace("\n"," ") for i in driver.find_elements(By.CSS_SELECTOR,'div.area')] 
print(area_lis,len(area_lis))

# loc_lis = [ i.text for i in driver.find_elements('div.result-content > div.location')]
# print(loc_lis)

## ราคา
price_lis = [ i.text for i in driver.find_elements(By.CSS_SELECTOR,'p.spacial-price')]
print(price_lis,len(price_lis))

#location
loc_lis = [ i.text for i in driver.find_elements(By.CSS_SELECTOR,'.result-content > div.location')]
print(loc_lis,len(loc_lis))

sub_district_lis = []
prov_lis = []

for loc in loc_lis:
    try:
        sub_district = loc.split(" ")[0]
    
        print(sub_district)
        logging.debug(f"Sub District : {sub_district}")
    except:
        sub_district = "ไม่มี"
        logging.warning("ไม่มี")

    sub_district_lis.append(sub_district)

    try:
        province = loc.split(" ")[1] 
        print(province)
        logging.debug(f"Province : {province}")
    
    except: 
        province = "ไม่มี"
        logging.warning("ไม่มี")

    prov_lis.append(province)

print(sub_district_lis,len(sub_district_lis))
print(prov_lis,len(prov_lis))


#name
name_lis = []

#property type
prop_lis = []


lat_lis = []
long_lis = []

print(len(lis))
print(lis,len(lis))


for x in lis: 

    driver.get(x)

    name = driver.find_element(By.CSS_SELECTOR,'p.current-page').text 
    name_lis.append(name)
    print(name)
    logging.debug(f"Name : {name}")

    proptype = driver.find_element(By.CSS_SELECTOR,'div.property-details').find_elements(By.CSS_SELECTOR,'div.property-td')[1].text 
    prop_lis.append(proptype)
    print(proptype)
    logging.debug(f"Proptype : {proptype}")


    lat_long = driver.find_element(By.CSS_SELECTOR,'.property-info-w').find_elements(By.CSS_SELECTOR,'.property-td')[-1].text.split("\n")
    
    print(lat_long)
    logging.debug(f"Lat and Long : {lat_long}")

    lat_lis.append(lat_long[0])

    long_lis.append(lat_long[1])




df = pd.DataFrame()
df['Name'] = name_lis[:len(lis)]
df['Link'] = lis[:len(lis)]
df['area'] = area_lis[:len(lis)]
df['Price'] = price_lis[:len(lis)]
df['Lat'] = lat_lis[:len(lis)]
df['Long'] = long_lis[:len(lis)]
df['Address'] = loc_lis[:len(lis)]
df['Province'] = prov_lis[:len(lis)]
df['District'] = sub_district_lis[:len(lis)]
df['Sub District'] = sub_district_lis[:len(lis)] 
df['image'] = img_lis[:len(lis)] 

# remove null row
df.dropna()
df.to_excel(filename)

if len(name_lis) == 0:
    logging.error("Error Scraping , Please check the website layout!!")
else: 
    logging.info('Done Scraping without Error')
