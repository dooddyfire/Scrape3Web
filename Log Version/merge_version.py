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
    

# Create loggers for each function
ghb_logger = logging.getLogger('ghb_logger')
ghb_logger.setLevel(logging.DEBUG)

bangkok_logger = logging.getLogger('bangkok_logger')
bangkok_logger.setLevel(logging.DEBUG)

kasikorn_logger = logging.getLogger('kasikorn_logger')
kasikorn_logger.setLevel(logging.DEBUG)

bam_logger = logging.getLogger('bam_logger')
bam_logger.setLevel(logging.DEBUG)


# Create file handlers for each logger
ghb_file_handler = logging.FileHandler(f'ghb_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
ghb_file_handler.setLevel(logging.DEBUG)

bangkok_file_handler = logging.FileHandler(f'bangkok_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
bangkok_file_handler.setLevel(logging.DEBUG)

kasikorn_file_handler = logging.FileHandler(f'kasikorn_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
kasikorn_file_handler.setLevel(logging.DEBUG)

bam_file_handler = logging.FileHandler(f'bam_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log_')
bam_file_handler.setLevel(logging.DEBUG)

# Create formatters
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add formatter to file handlers
ghb_file_handler.setFormatter(formatter)
bangkok_file_handler.setFormatter(formatter)
kasikorn_file_handler.setFormatter(formatter)
bam_file_handler.setFormatter(formatter)

# Add file handlers to loggers
ghb_logger.addHandler(ghb_file_handler)
bangkok_logger.addHandler(bangkok_file_handler)
kasikorn_logger.addHandler(kasikorn_file_handler)
bam_logger.addHandler(bam_file_handler)



def scrape_ghb(start_page):
    
    # ชื่อไฟล์
    filename = f'scrape_ghb{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'


    log_file = f'logging_bangkok_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'


    # option headless
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    linkx = "https://www.ghbhomecenter.com/property-for-sale"
    driver.get(linkx)

    lisqp = [ h.text for h in driver.find_elements(By.CSS_SELECTOR,'a.page-link')]
    print(lisqp)
    ghb_logger.debug(f"{lisqp}")

    # หน้าเริ่มต้น
    start = start_page

    # หน้าสุดท้าย เซตหน้าสุดท้าย
    #end = int(lisqp[-2])
    
    # เซต test
    end = 3
    print("End Page : {}".format(end))
    ghb_logger.info(f"End Page : {end}")


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
        url = "https://www.ghbhomecenter.com/property-for-sale?&pg={}".format(i)
        driver.get(url)



        soup = BeautifulSoup(driver.page_source,'html.parser')


        lis = [x['rel'] for x in soup.find_all('div',{'class':'link-property-detail'})]

        print("Page : ",i)
        ghb_logger.info(f"Page : {i}")


        area_lisx = [f.find('div',{'class':'text-area'}).text.strip() for f in soup.find_all('div',{'class':'link-property-detail'})]
        for a in area_lisx: 

            area_lis.append(a)
            print(a)

            #logging.debug(f"{a}")





        for u in lis: 

            url_lis.append(u)
            print(u)
            ghb_logger.debug(f"Url : {u}")



            driver.get(u)
            soupx = BeautifulSoup(driver.page_source,'html.parser')

            sect = soupx.find('section',{'class':'page-product-detail'})

            try:
                img = soupx.find('div',{'class':'img-fill'}).find('img')['src']
                image_lis.append(img)
                print(img)
                ghb_logger.debug(f"Img : {img}")

            except: 
                img = " "
                image_lis.append(img)
                print(img)
                ghb_logger.warning("img : ไม่มี")

            try:
                name = sect.find('h1').text 
                name_lis.append(name)
                print(name)
                ghb_logger.debug(f"Name : {name}")
            except: 
                name = " "
                name_lis.append(name)
                print(name)
                ghb_logger.warning(f"Name : ไม่มี")


            try:
                price = sect.find('h3',{'class':'text-price'}).text.replace("ราคาทรัพย์","").strip()
                ghb_logger.debug(f"Price : {price}")
                
            except: 
                price = " "
            print(price)
            price_lis.append(price)

            lisx = [ g for g in sect.find_all('li',{'class':'list-group-item'})]
            print(lisx)

            try:
                typex = lisx[0].text.strip()
                ghb_logger.debug(f"Type : {typex}")
            except: 
                typex = " "
            
            print(typex)
            type_lis.append(typex)

            try:
                province = lisx[5].text.replace("จังหวัด","").strip()
                ghb_logger.debug(f"Province : {province}")
            except:
                province = " "

            prov_lis.append(province)
            print(province)

            try:
                district = lisx[-2].text.strip()
                ghb_logger.debug(f"District : {district}")
            except: 
                district = " "

            
            district_lis.append(district)
            print(district)

            try:
                subdis = lisx[4].text.strip()
                ghb_logger.debug(f"Sub District : {subdis}")
            except:
                subdis = " "
            subdistrict_lis.append(subdis)
            print(subdis)

            try:
                address = subdis +" " +district+" "+province
                ghb_logger.debug(f"Address : {address}")
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
                    lat = float(match.group(1))
                    long = float(match.group(2))
                    print("Latitude:", lat)
                    ghb_logger.debug(f"Lat : {lat}")
                    print("Longitude:", long)
                    ghb_logger.debug(f"Longitude : {long}")

                else:
                    lat = " "
                    long = " "
                    print("No latitude and longitude found in the link.")
                    ghb_logger.warning("No latitude and longitude found in the link.")

            lat_lis.append(lat)
            long_lis.append(long)     

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
        ghb_logger.error("Error Scraping , Please check the website layout!!")
    else: 
        ghb_logger.info('Done Scraping without Error')



def scrape_bangkok():

    # set logging file 
        
    # ชื่อไฟล์
    filename = f'scrape_bangkok_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

    log_file = f'logging_bangkok_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'



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
    total_item = 10
    bangkok_logger.info("Total Scrape Item : {}".format(total_item))

    count = 1  
    for x in url_lis: 
        # test debug
        if count == total_item: 
            break
        

        bangkok_logger.info("-------------------- Item {} -----------------".format(count))
        bangkok_logger.debug(x)
        driver.get(x)
        time.sleep(3)
        lisx = driver.find_elements(By.CSS_SELECTOR,'label')




        for tag in lisx:
            bangkok_logger.debug(tag.text)

        # img = driver.find_element(By.CSS_SELECTOR,'div.item slick-slide ').find_element(By.CSS_SELECTOR,'img').get_attribute('href') 
        # print(img)

        lis_link = driver.find_elements(By.CSS_SELECTOR,'a')
        gmap = [ d.get_attribute('href') for d in lis_link][145]
        bangkok_logger.debug(gmap)



        custom = [ x for x in lisx]
        bangkok_logger.info(f"Total Custom : {len(custom)}")
        try:
            linkdd = driver.current_url

            name = custom[1].text
            bangkok_logger.debug(name)

            proptype = custom[3].text
            bangkok_logger.debug(proptype)

            img = driver.find_element(By.CSS_SELECTOR,'img#image-five-1').get_attribute('src')
            bangkok_logger.debug(img)

            area = str(custom[5].text)+ " ไร่ " + str(custom[6].text) + " งาน " + str(custom[7].text) + " ตร.วา " + str(custom[8].text) + " ตร.เมตร "
            bangkok_logger.debug(area)

            price = custom[16].text
            bangkok_logger.debug(price)

            

            address = custom[14].text
            bangkok_logger.debug("Address : {}".format(address))

            province = custom[14].text.split(" ")[-1]
            bangkok_logger.debug(province)
        except: 
            bangkok_logger.warning("Skip")
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

    bangkok_logger.debug(gmap_main_lis)
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
        bangkok_logger.debug(f"Lat : {lat}")
                
        long = lat_longx[1]
        bangkok_logger.debug(f"Long : {long}") 

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


    if len(name_lis) == 0:
        bangkok_logger.error("Error Scraping , Please check the website layout!!")
    else: 
        bangkok_logger.info('Done Scraping without Error')


def scrape_bam():
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

            bam_logger.debug(f"Link {link}")

            #Name
            name = driver.find_element(By.CSS_SELECTOR,'span.sc-dkPtRN').text
            print(name)
            name_lis.append(name)

            bam_logger.debug(f"Name {name}")

            #Price
            price = driver.find_element(By.CSS_SELECTOR,'span.egCfYl').text 
            print(price)
            price_lis.append(price)

            bam_logger.debug(f"Price {price}")

            img = driver.find_element(By.CSS_SELECTOR,'div.sc-kfPuZi').get_attribute('src')
            print(img)
            img_lis.append(img)

            bam_logger.debug(f"Image {img}")

            area = [ p.text for p in driver.find_elements(By.CSS_SELECTOR,'span.sc-gsDKAQ')][13]
            print(area)
            area_lis.append(area)

            bam_logger.debug(f"Area {area}")


            # loc = driver.find_element(By.CSS_SELECTOR,'span.WtLyf').text 
            # print(loc)
            customx = [ g.text for g in driver.find_elements(By.CSS_SELECTOR,'div.hfuCGv')]
            print(customx)

            loc = customx[4]
            print(loc)
            loc_lis.append(loc)
            bam_logger.debug(f"Location {loc}")

            province = customx[5]
            print(province)
            prov_lis.append(province)
            bam_logger.debug(f"Province {province}")

            sub_distrct = customx[6]
            print(sub_distrct)
            sub_district_lis.append(sub_distrct)
            bam_logger.debug(f"Sub District : {sub_distrct}")

            #Proptype
            proptype = driver.find_element(By.CSS_SELECTOR,'.sc-crHmcD .dOfHNG').text
            print(proptype)
            prop_lis.append(proptype)
            bam_logger.debug(f"Proptype : {proptype}")

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
            bam_logger.debug(f"Lat {lat}")

            long = lat_long.split(",")[1]
            print("Long : ",long)
            long_lis.append(long)
            bam_logger.debug(f"Long {long}")
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
        bam_logger.error("Error Scraping , Please check the website layout!!")
    else: 
        bam_logger.info('Done Scraping without Error')


def scrape_kasikorn():
   
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
            kasikorn_logger.debug(f"Sub District : {sub_district}")
        except:
            sub_district = "ไม่มี"
            kasikorn_logger.warning("ไม่มี")

        sub_district_lis.append(sub_district)

        try:
            province = loc.split(" ")[1] 
            print(province)
            kasikorn_logger.debug(f"Province : {province}")
        
        except: 
            province = "ไม่มี"
            kasikorn_logger.warning("ไม่มี")

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
        kasikorn_logger.debug(f"Name : {name}")

        proptype = driver.find_element(By.CSS_SELECTOR,'div.property-details').find_elements(By.CSS_SELECTOR,'div.property-td')[1].text 
        prop_lis.append(proptype)
        print(proptype)
        kasikorn_logger.debug(f"Proptype : {proptype}")


        lat_long = driver.find_element(By.CSS_SELECTOR,'.property-info-w').find_elements(By.CSS_SELECTOR,'.property-td')[-1].text.split("\n")
        
        print(lat_long)
        kasikorn_logger.debug(f"Lat and Long : {lat_long}")

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
        kasikorn_logger.error("Error Scraping , Please check the website layout!!")
    else: 
        kasikorn_logger.info('Done Scraping without Error')


    #=============== insert database after this ============================
scrape_ghb(1)
scrape_bam()
scrape_bangkok()
scrape_kasikorn()

print("All done")