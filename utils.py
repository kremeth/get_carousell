from selenium.webdriver.firefox.options import Options
import flask
import re
import string
import sys
from collections import namedtuple as _namedtuple
import pymysql
import ssl
import time
from selenium import webdriver
import re
import pandas as pd
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from rq import Worker, Queue, Connection
from worker import conn


def get_closest_utils(name):


    # r = requests.get(
    #     f'https://www.vestiairecollective.com/search/?q={val}#sold=1', headers=headers)

    options = Options()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument('--window-size=1920,1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

    # options = Options()
    # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # options.add_argument('--headless')
    # options.add_argument('--window-size=1920,1080')
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

    # driver = webdriver.Chrome(service=Service(
    #     ChromeDriverManager().install()), options=options, executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    driver.maximize_window()
    driver.get(f'https://www.carousell.sg/u/{name}/')


# options = Options()
# options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# options.add_argument("--headless")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--no-sandbox")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)



    # TODO: delete after

    # options = Options()
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

    # driver = webdriver.Chrome(service=Service(
    #     ChromeDriverManager().install()), options=options)
    # driver.maximize_window()

    # driver.get('https://www.carousell.sg/p/🖤-chanel-vintage-medium-cf-classic-flap-bag-black-25cm-25-cm-24k-ghw-gold-hardware-small-jumbo-mini-caviar-23cm-23-1170217760/?t-id=uWeXsJ6KXZ_1658515078357&t-referrer_request_id=V0lIz_d7Mk18P2VH&t-tap_index=0')



    # driver = webdriver.Chrome(service=Service(
    #     ChromeDriverManager().install()))
    # driver.get(f'https://www.carousell.sg/u/diamondquilting/')
    # Click the button


    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(5)
            btn = [val for val in driver.find_elements(
                By.CSS_SELECTOR, 'button') if val.text == 'View more'][0]
            btn.click()
            time.sleep(2)
            # driver.execute_script("arguments[0].click();", btn)
            # btn.find_element(By.XPATH, '..').click()
            # print(len(driver.find_elements(By.CSS_SELECTOR, 'a')))
            # time.sleep(2)
            # driver.implicitly_wait(1)
        except IndexError:
            # links = [val.get_attribute('href') for val in driver.find_elements(By.CSS_SELECTOR, 'a') if '/p/' in val.get_attribute('href')]
            # Filter out all the products
            links = [val for val in driver.find_elements(By.CSS_SELECTOR, 'a') if '/p/' in val.get_attribute('href')]
            # Get only the items that are not sold yet
            links = [val for val in links if 'SOLD' not in val.text]
            # 
            # links = list(itertools.chain.from_iterable([[val.get_attribute('href') for val in links if ele in val.text] for ele in brands]))
            links = [val.get_attribute('href') for val in links]
            break


    rows = []
    for link in tqdm(links):
        driver.get(link)
        # time.sleep(5)
        title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[1]/p').text
        price = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[1]/section/div/div/div/div/div/div/h2').text
        # description = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[2]/section').text
        # category = ''
        # try:
        #     category = description.split('\n')[description.split('\n').index('Type')+1]
        # except:
        #     pass
        # try:
        #     brand = description.split('\n')[description.split('\n').index('Brand')+1]
        # except:
        #     brand = ''
        # try:
        #     condition = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/section/div/div/div').text.split('\nMailing')[0]
        # except:
        #     pass
        text_listing = [val.text for val in driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[2]/section').find_elements(By.CSS_SELECTOR, 'p')]
        try:
            brand = text_listing[text_listing.index('Brand')+1]
        except:
            brand = ''
        try:
            model = text_listing[text_listing.index('Model')+1]
        except:
            model = ''
        try:
            category = text_listing[text_listing.index('Type')+1]
        except:
            category = ''
        try:
            accessories = text_listing[text_listing.index('Accessories')+1]
        except:
            accessories = ''
        try:
            description = text_listing[text_listing.index('Description')+1]
        except:
            description = ''
        try:
            images = '; '.join([val.get_attribute('src') for val in driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/section/div/div/div').find_elements(By.CSS_SELECTOR, 'img')])
        except:
            images = ''
        

        row = {
            'title': title,
            'price': price,
            'brand': brand,
            'model': model,
            'category': category,
            'accessories': accessories,
            'description': description,
            'images': images
        }

        rows.append(row)

        pd.DataFrame(rows).to_csv('/Users/mathieukremeth/Desktop/dcarousell_extract.csv')

        data = pd.read_csv('/Users/mathieukremeth/Desktop/dcarousell_extract.csv', index_col=0)

        # Filter by brands
        data = data[data['brand'].isin(brands)]

        # Filter by category

        return data.to_json()
