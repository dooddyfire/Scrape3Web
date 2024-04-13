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

main_url = "https://www.bam.co.th/search?pageSize=12&pageNumber=1&groupType=%E0%B8%97%E0%B8%A3%E0%B8%B1%E0%B8%9E%E0%B8%A2%E0%B9%8C%E0%B8%A3%E0%B8%B2%E0%B8%84%E0%B8%B2%E0%B8%9E%E0%B8%B4%E0%B9%80%E0%B8%A8%E0%B8%A9&campaignName="

url_lis = []

driver.get(main_url)

driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
time.sleep(3)

start = 1 
end = 3

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


        link = driver.current_url 
        url_lis.append(link)
        print(link)


        name = driver.find_element(By.CSS_SELECTOR,'span.sc-dkPtRN').text
        print(name)

        price = driver.find_element(By.CSS_SELECTOR,'span.egCfYl').text 
        print(price)

        # loc = driver.find_element(By.CSS_SELECTOR,'span.WtLyf').text 
        # print(loc)


        proptype = driver.find_element(By.CSS_SELECTOR,'.sc-crHmcD .dOfHNG').text
        print(proptype)

        # Google Map
        google_maps_pattern = r"https?://(?:www\.)?google\.com/maps/search/\?.*"

        # Assuming driver.page_source contains the HTML source
        html_source = driver.page_source

        # Parse the HTML source using BeautifulSoup
        soup = BeautifulSoup(html_source, 'html.parser')

        # Find all anchor elements with href attribute containing 'maps.google.com'
        google_map_links = soup.find_all('a', href=re.compile(google_maps_pattern))

        # Extract and print the Google Maps links
        for link in google_map_links:
            google_maps_link = link['href']
            print("Google Maps link:", google_maps_link)

        
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

