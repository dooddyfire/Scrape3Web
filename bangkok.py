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
gmap_main_lis = []
gmap_correct_lis = []


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


# option headless
options = Options()
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Set Fix Total Item 
total_item = 500

count = 1  
for x in url_lis: 
    # test debug
    if count == total_item: 
        break
    
    print("-------------------- Item {} -----------------".format(count))
    print(x)
    driver.get(x)
    time.sleep(3)
    lisx = driver.find_elements(By.CSS_SELECTOR,'label')




    for tag in lisx:
        print(tag.text)

    # img = driver.find_element(By.CSS_SELECTOR,'div.item slick-slide ').find_element(By.CSS_SELECTOR,'img').get_attribute('href') 
    # print(img)

    lis_link = driver.find_elements(By.CSS_SELECTOR,'a')
    gmap = [ d.get_attribute('href') for d in lis_link][145]
    print(gmap)



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

        

        address = custom[14].text
        print("Address : ",address)

        province = custom[14].text.split(" ")[-1]
        print(province)
    except: 
        print("Skip")
        continue

    count = count + 1



    name_lis.append(name)
    link_lis.append(linkdd)
    area_lis.append(area)
    price_lis.append(price)

    loc_lis.append(address)
    prov_lis.append(province)
    sub_district_lis.append(province)
    img_lis.append(img)
    prop_lis.append(proptype)


    gmap_main_lis.append(gmap)

print(gmap_main_lis)
for google_map in gmap_main_lis: 
    driver.get(google_map)

    time.sleep(3)
    btn_search = driver.find_element(By.CSS_SELECTOR,'#searchbox-searchbutton')
    btn_search.click()

    time.sleep(3)
    lat_longx = driver.find_element(By.CSS_SELECTOR,'h2.bwoZTb').text
    print(lat_longx)

    lat_longx = lat_longx.split(",")

    lat = lat_longx[0]
    print("Lat : ",lat)
            
    long = lat_longx[1]
    print("Long : ",long) 

    lat_lis.append(lat)
    long_lis.append(long)

    gmap_correct = f"https://www.google.co.th/maps/place/{lat},{long}"
    gmap_correct_lis.append(gmap_correct)

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
df['Google Map'] = gmap_correct_lis

# remove null row
df.dropna()
df.to_excel(filename)

    # proptype = driver.find_element(By.CSS_SELECTOR,'#lblPropertyType').text 
    # print(proptype)
