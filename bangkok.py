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



    
# ชื่อไฟล์
filename = f'scrape_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'



# option headless
options = Options()
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


start = 1 
end = 1 
url_lis = []

name_lis = []
link_lis = []
area_lis = []
price_lis = []
lat_lis = []
long_lis = []
loc_lis = []
prov_lis = []
sub_district_lis = []
img_lis = []
area_lis = []
prop_lis = []

for page in range(start,end+1): 

    driver.get('https://www.bangkokbank.com/th-TH/Property-For-Sale#page-{}'.format(page))
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    
    print(driver.page_source)

    lis = driver.find_elements(By.CSS_SELECTOR,'a.btn-primary')

    
    for i in lis: 
        url = i.get_attribute('href')
        #print(url)

        if url: 
            #print(url)
            url_lis.append(url)

        # driver.get(url)
        # time.sleep(3)
        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        

        # print(driver.page_source)
        # proptype = driver.find_element(By.CSS_SELECTOR,'label#lblPropertyType').text         
        # print(proptype)

# option headless
options = Options()
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)




for x in url_lis: 

    print(x)
    driver.get(x)
    time.sleep(3)
    lisx = driver.find_elements(By.CSS_SELECTOR,'label')




    for tag in lisx:
        print(tag.text)

    # img = driver.find_element(By.CSS_SELECTOR,'div.item slick-slide ').find_element(By.CSS_SELECTOR,'img').get_attribute('href') 
    # print(img)

    lis_link = driver.find_elements(By.CSS_SELECTOR,'a')
    lat_long = [ d.get_attribute('href') for d in lis_link][145]
    print(lat_long)



    custom = [ x for x in lisx]
    print("Total Custom : ",len(custom))
    try:
        linkdd = driver.current_url

        name = custom[1].text
        print(name)

        proptype = custom[3].text
        print(proptype)

        img = driver.find_element(By.CSS_SELECTOR,'img#image-five-1').get_attribute('src')
        print(img)

        area = str(custom[5].text)+ " ไร่ " + str(custom[6].text) + " งาน " + str(custom[7].text) + " ตร.วา " + str(custom[8].text) + " ตร.เมตร "
        print(area)

        price = custom[16].text
        print(price)

        lat =  lat_long
        print("Lat : ",lat)

        long = lat_long
        print("Long : ",long)

        address = custom[14].text
        print("Address : ",address)

        province = custom[14].text.split(" ")[-1]
        print(province)
    except: 
        print("Skip")
        continue
    name_lis.append(name)
    link_lis.append(linkdd)
    area_lis.append(area)
    price_lis.append(price)
    lat_lis.append(lat_long)
    long_lis.append(lat_long)
    loc_lis.append(address)
    prov_lis.append(province)
    sub_district_lis.append(province)
    img_lis.append(img)
    prop_lis.append(proptype)

df = pd.DataFrame()
df['Name'] = name_lis
df['Link'] = link_lis
df['area'] = area_lis
df['Price'] = price_lis
df['Lat'] = lat_lis
df['Long'] = long_lis
df['Address'] = loc_lis
df['Province'] = prov_lis
df['District'] = sub_district_lis
df['Sub District'] = sub_district_lis 
df['image'] = img_lis

df.to_excel(filename)

    # proptype = driver.find_element(By.CSS_SELECTOR,'#lblPropertyType').text 
    # print(proptype)
