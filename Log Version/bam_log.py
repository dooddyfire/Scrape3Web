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
filename = f'scrape_bam_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
log_file = f'logging_bam_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'



# option headless
options = Options()
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

main_url = "https://www.bam.co.th/search?pageSize=12&pageNumber=1&groupType=%E0%B8%97%E0%B8%A3%E0%B8%B1%E0%B8%9E%E0%B8%A2%E0%B9%8C%E0%B8%A3%E0%B8%B2%E0%B8%84%E0%B8%B2%E0%B8%9E%E0%B8%B4%E0%B9%80%E0%B8%A8%E0%B8%A9&campaignName="

url_lis = []

driver.get(main_url)

driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
time.sleep(3)

start = 1 
end = 2 # end page 


df = pd.DataFrame()
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


    # scrape_item from current page 
    lis = driver.find_elements(By.CSS_SELECTOR,'.d-flex.col-6.col-md-3.p-1.p-md-0.justify-content-center')
    print(lis)


    #retrieve each item data
    for item in lis: 
        #print(item.get_attribute('innerHTML'))
        driver.execute_script("arguments[0].click();", item)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

        #switch to new tab
        driver.switch_to.window(driver.window_handles[-1])
        # Link 
        link = driver.current_url 
        url_lis.append(link)
        print(link)

        logging.debug(f"Link {link}")

        #Name
        name = driver.find_element(By.CSS_SELECTOR,'span.sc-dkPtRN').text
        print(name)
        name_lis.append(name)

        logging.debug(f"Name {name}")

        #Price
        price = driver.find_element(By.CSS_SELECTOR,'span.egCfYl').text 
        print(price)
        price_lis.append(price)

        logging.debug(f"Price {price}")

        img = driver.find_element(By.CSS_SELECTOR,'div.sc-kfPuZi').get_attribute('src')
        print(img)
        img_lis.append(img)

        logging.debug(f"Image {img}")

        area = [ p.text for p in driver.find_elements(By.CSS_SELECTOR,'span.sc-gsDKAQ')][13]
        print(area)
        area_lis.append(area)

        logging.debug(f"Area {area}")


        # loc = driver.find_element(By.CSS_SELECTOR,'span.WtLyf').text 
        # print(loc)
        customx = [ g.text for g in driver.find_elements(By.CSS_SELECTOR,'div.hfuCGv')]
        print(customx)

        loc = customx[4]
        print(loc)
        loc_lis.append(loc)
        logging.debug(f"Location {loc}")

        province = customx[5]
        print(province)
        prov_lis.append(province)
        logging.debug(f"Province {province}")

        sub_distrct = customx[6]
        print(sub_distrct)
        sub_district_lis.append(sub_distrct)
        logging.debug(f"Sub District : {sub_distrct}")

        #Proptype
        proptype = driver.find_element(By.CSS_SELECTOR,'.sc-crHmcD .dOfHNG').text
        print(proptype)
        prop_lis.append(proptype)
        logging.debug(f"Proptype : {proptype}")

        # Google Map
        google_maps_pattern = r"https?://(?:www\.)?google\.com/maps/search/\?.*"

        # Assuming driver.page_source contains the HTML source
        html_source = driver.page_source

        # Parse the HTML source using BeautifulSoup
        soup = BeautifulSoup(html_source, 'html.parser')

        # Find all anchor elements with href attribute containing 'maps.google.com'
        google_map_links = soup.find_all('a', href=re.compile(google_maps_pattern))

        # Extract and print the Google Maps links
        for linkx in google_map_links:
            google_maps_link = linkx['href']
            print("Google Maps link:", google_maps_link)
            
        lat_long = google_maps_link.split("=")[-1]

        lat = lat_long.split(",")[0]
        print("Lat : ",lat)
        lat_lis.append(lat)
        logging.debug(f"Lat {lat}")

        long = lat_long.split(",")[1]
        print("Long : ",long)
        long_lis.append(long)
        logging.debug(f"Long {long}")
        # switch back to original tab
        driver.switch_to.window(driver.window_handles[0])
        # Get the current window handle
        current_window = driver.current_window_handle

        # Get all window handles
        all_windows = driver.window_handles

        # Iterate through all windows
        for window in all_windows:
            # Switch to the window
            driver.switch_to.window(window)
            # Close the window if it's not the current window
            if window != current_window:
                driver.close()

        # Switch back to the original tab
        driver.switch_to.window(current_window)


    btn_next = driver.find_element(By.CSS_SELECTOR,'button.pagination-next')
    driver.execute_script("arguments[0].click();", btn_next)   

df = pd.DataFrame()
df['Name'] = name_lis
df['Link'] = url_lis 
df['area'] = area_lis
df['Price'] = price_lis
df['Lat'] = lat_lis
df['Long'] = long_lis
df['Address'] = loc_lis
df['Province'] = prov_lis
df['District'] = sub_district_lis
df['Sub District'] = sub_district_lis 
df['image'] = img_lis
df['Type'] = prop_lis 

# remove null row
df.dropna()
df.to_excel(filename)

if len(name_lis) == 0:
    logging.error("Error Scraping , Please check the website layout!!")
else: 
    logging.info('Done Scraping without Error')