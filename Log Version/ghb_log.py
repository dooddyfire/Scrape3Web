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

# set logging file 
    



def scrape_data(start_page):
    
    # ชื่อไฟล์
    filename = f'scrape_ghb{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'


    log_file = f'logging_bangkok_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(filename=log_file,level=logging.DEBUG, filemode='w', format='%(name)s - %(levelname)s - %(message)s')


    # option headless
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    linkx = "https://www.ghbhomecenter.com/property-for-sale?&pId=395&pg=1"
    driver.get(linkx)

    lisqp = [ h.text for h in driver.find_elements(By.CSS_SELECTOR,'a.page-link')]
    print(lisqp)
    logging.debug(f"{lisqp}")

    # หน้าเริ่มต้น
    start = start_page
    # หน้าสุดท้าย เซตหน้าสุดท้าย
    end = int(lisqp[-2])
    print("End Page : {}".format(end))
    logging.info(f"End Page : {end}")


    area_lis = []
    map_link = []
    lat_lis = []
    long_lis = []
    url_lis = []

    img_lis = []
    type_lis = []
    price_lis = []
    address_lis = []
    prov_lis = []
    district_lis = []
    subdistrict_lis = []
    source_lis = []
    web_lis = []
    image_lis = []
    address_lis = []
    name_lis = []
    gmap_lis = []

    for i in range(start,end+1):
        # ลิงค์
        url = "https://www.ghbhomecenter.com/property-for-sale?&pId=395&pg={}".format(i)
        driver.get(url)



        soup = BeautifulSoup(driver.page_source,'html.parser')


        lis = [x['rel'] for x in soup.find_all('div',{'class':'link-property-detail'})]

        print("Page : ",i)
        logging.info(f"Page : {i}")


        area_lisx = [f.find('div',{'class':'text-area'}).text.strip() for f in soup.find_all('div',{'class':'link-property-detail'})]
        for a in area_lisx: 

            area_lis.append(a)
            print(a)

            logging.debug(f"{a}")





        for u in lis: 

            url_lis.append(u)
            print(u)
            logging.debug(f"Url : {u}")



            driver.get(u)
            soupx = BeautifulSoup(driver.page_source,'html.parser')

            sect = soupx.find('section',{'class':'page-product-detail'})

            try:
                img = soupx.find('div',{'class':'img-fill'}).find('img')['src']
                image_lis.append(img)
                print(img)
                logging.debug(f"Img : {img}")

            except: 
                img = " "
                image_lis.append(img)
                print(img)
                logging.warning("img : ไม่มี")

            try:
                name = sect.find('h1').text 
                name_lis.append(name)
                print(name)
                logging.debug(f"Name : {name}")
            except: 
                name = " "
                name_lis.append(name)
                print(name)
                logging.warning(f"Name : ไม่มี")


            try:
                price = sect.find('h3',{'class':'text-price'}).text.replace("ราคาทรัพย์","").strip()
                logging.debug(f"Price : {price}")
                
            except: 
                price = " "
            print(price)
            price_lis.append(price)

            lisx = [ g for g in sect.find_all('li',{'class':'list-group-item'})]
            print(lisx)

            try:
                typex = lisx[0].text.strip()
                logging.debug(f"Type : {typex}")
            except: 
                typex = " "
            
            print(typex)
            type_lis.append(typex)

            try:
                province = lisx[5].text.replace("จังหวัด","").strip()
                logging.debug(f"Province : {province}")
            except:
                province = " "

            prov_lis.append(province)
            print(province)

            try:
                district = lisx[-2].text.strip()
                logging.debug(f"District : {district}")
            except: 
                district = " "

            
            district_lis.append(district)
            print(district)

            try:
                subdis = lisx[4].text.strip()
                logging.debug(f"Sub District : {subdis}")
            except:
                subdis = " "
            subdistrict_lis.append(subdis)
            print(subdis)

            try:
                address = subdis +" " +district+" "+province
                logging.debug(f"Address : {address}")
            except: 
                address = " "

            
            print(address)
            address_lis.append(address)

            google_maps_regex = re.compile(r'https?://(?:www\.)?google\.com/maps\?.*')

            # Extracting Google Maps links from HTML content
            google_maps_links = google_maps_regex.findall(driver.page_source)

            # Output the extracted links
            if len(google_maps_links) == 0: 
                lat = " "
                long = " "
            else: 
                # Regular expression to extract latitude and longitude values
                google_maps_link = google_maps_links[0]

                gmap_lis.append(google_maps_link)

                lat_long_regex = re.compile(r'daddr=(-?\d+\.\d+),(-?\d+\.\d+)')

                # Extract latitude and longitude values from the Google Maps link
                match = lat_long_regex.search(google_maps_link)

                if match:
                    latitude = float(match.group(1))
                    longitude = float(match.group(2))
                    print("Latitude:", latitude)
                    logging.debug(f"Lat : {latitude}")
                    print("Longitude:", longitude)
                    logging.debug(f"Longitude : {longitude}")

                else:
                    lat = " "
                    long = " "
                    print("No latitude and longitude found in the link.")
                    logging.warning("No latitude and longitude found in the link.")

            lat_lis.append(latitude)
            long_lis.append(longitude)     

            print("---------------------")

    print(len(image_lis))
    print(len(url_lis))
    df = pd.DataFrame()

    df['name'] = name_lis 
    df['link'] = url_lis 
    df['type'] = type_lis 
    df['area'] = area_lis 
    df['price'] = price_lis 
    df['lat'] = lat_lis 
    df['long'] = long_lis 
    df['address'] = address_lis 
    df['province'] = prov_lis 
    df['district'] = district_lis 
    df['subdistrict'] = subdistrict_lis 
    df['image'] = image_lis

    df.to_excel(filename)

    print("finish")
    
    if len(name_lis) == 0:
        logging.error("Error Scraping , Please check the website layout!!")
    else: 
        logging.info('Done Scraping without Error')



    #=============== insert database after this ============================
scrape_data(1)