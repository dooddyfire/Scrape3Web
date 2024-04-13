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

for page in range(start,end+2): 

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

    # proptype = driver.find_element(By.CSS_SELECTOR,'#lblPropertyType').text 
    # print(proptype)
