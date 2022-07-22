from selenium.webdriver.firefox.options import Options
import flask
import urllib.request
import re
import string
import sys
from collections import namedtuple as _namedtuple
import pymysql
import ssl
import requests
import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re
import itertools
import pandas as pd
import numpy as np
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from lxml import etree
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm
import time
from selenium.webdriver.common.keys import Keys
import selenium
import shutil
import urllib.request
import os
import ast
from webflowpy.Webflow import Webflow
from webflowpy.WebflowResponse import WebflowResponse
from webflowpy.utils import requests_retry_session
import cloudscraper
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains


ssl._create_default_https_context = ssl._create_unverified_context

connection = pymysql.connect(
    host='34.142.176.229', user='root', password='HAM1qzn-gyt7pae-agj', db='stylebase')
cursor = connection.cursor()

cursor.execute('SELECT reference_field FROM Items;')
comp = '|||'.join([val[0] for val in cursor.fetchall()])

app = flask.Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return "waiting"


@app.route('/<string:name>')
def get_closest(name):


    # r = requests.get(
    #     f'https://www.vestiairecollective.com/search/?q={val}#sold=1', headers=headers)

    options = Options()

    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    driver.get(f'https://www.carousell.sg/u/{name}/')



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





brands = ['Versace',
          'Van Cleef & Arpels',
          'Valentino',
          'Tom Ford',
          'Tod\'s',
          'Tiffany & Co.',
          'The Row',
          'Telfar',
          'Stella McCartney',
          'Salvatore Ferragamo',
          'Saint Laurent',
          'Rolex',
          'Ralph Lauren Collection',
          'Proenza Schouler',
          'Prada',
          'Off White',
          'Nancy Gonzalez',
          'Mulberry',
          'Miu Miu',
          'Mark Cross',
          'Mansur Gavriel',
          'M2Malletier',
          'Louis Vuitton',
          'Loewe',
          'Lanvin',
          'Judith Leiber',
          'Jimmy Choo',
          'Jacquemus',
          'Hermes',
          'Harry Winston',
          'Gucci',
          'Goyard',
          'Givenchy',
          'Fendi',
          'Dolce & Gabbana',
          'Delvaux',
          'Christian Louboutin',
          'Christian Dior',
          'Chloe',
          'Chanel',
          'Celine',
          'Cartier',
          'Bvlgari',
          'Burberry',
          'Bottega Veneta',
          'Balenciaga',
          'Alexander Wang',
          'Alexander McQueen',
          'Alaia',
          '3.1 Phillip Lim']

PY3 = sys.version_info[0] == 3
if PY3:
    string = str


def token_set_ratio(s1, s2, force_ascii=True, full_process=True):
    return _token_set(s1, s2, partial=False, force_ascii=force_ascii, full_process=full_process)


def _token_set(s1, s2, partial=True, force_ascii=True, full_process=True):
    if not full_process and s1 == s2:
        return 100

    p1 = full_process_func(s1, force_ascii=force_ascii) if full_process else s1
    p2 = full_process_func(s2, force_ascii=force_ascii) if full_process else s2

    if not validate_string(p1):
        return 0
    if not validate_string(p2):
        return 0

    tokens1 = set(p1.split())
    tokens2 = set(p2.split())

    intersection = tokens1.intersection(tokens2)
    diff1to2 = tokens1.difference(tokens2)
    diff2to1 = tokens2.difference(tokens1)

    sorted_sect = " ".join(sorted(intersection))
    sorted_1to2 = " ".join(sorted(diff1to2))
    sorted_2to1 = " ".join(sorted(diff2to1))

    combined_1to2 = sorted_sect + " " + sorted_1to2
    combined_2to1 = sorted_sect + " " + sorted_2to1

    sorted_sect = sorted_sect.strip()
    combined_1to2 = combined_1to2.strip()
    combined_2to1 = combined_2to1.strip()

    ratio_func = ratio

    pairwise = [
        ratio_func(sorted_sect, combined_1to2),
        ratio_func(sorted_sect, combined_2to1),
        ratio_func(combined_1to2, combined_2to1)
    ]
    return max(pairwise)


def full_process_func(s, force_ascii=False):
    if force_ascii:
        s = asciidammit(s)
    string_out = StringProcessor.replace_non_letters_non_numbers_with_whitespace(
        s)
    string_out = StringProcessor.to_lower_case(string_out)
    string_out = StringProcessor.strip(string_out)
    return string_out


class StringProcessor(object):
    regex = re.compile(r"(?ui)\W")

    @classmethod
    def replace_non_letters_non_numbers_with_whitespace(cls, a_string):
        return cls.regex.sub(" ", a_string)

    strip = staticmethod(string.strip)
    to_lower_case = staticmethod(string.lower)
    to_upper_case = staticmethod(string.upper)


def asciidammit(s):
    if type(s) is str:
        return asciionly(s)
    elif type(s) is unicode:
        return asciionly(s.encode('ascii', 'ignore'))
    else:
        return asciidammit(unicode(s))


def asciionly(s):
    if PY3:
        return s.translate(translation_table)
    else:
        return s.translate(None, bad_chars)


PY3 = sys.version_info[0] == 3

bad_chars = str("").join([chr(i) for i in range(128, 256)])  # ascii dammit!
if PY3:
    translation_table = dict((ord(c), None) for c in bad_chars)
    unicode = str


def validate_string(s):
    try:
        return len(s) > 0
    except TypeError:
        return False


def intr(n):
    return int(round(n))


def ratio(s1, s2):
    s1, s2 = make_type_consistent(s1, s2)

    m = SequenceMatcher(None, s1, s2)
    return intr(100 * m.ratio())


def make_type_consistent(s1, s2):
    if isinstance(s1, str) and isinstance(s2, str):
        return s1, s2

    elif isinstance(s1, unicode) and isinstance(s2, unicode):
        return s1, s2

    else:
        return unicode(s1), unicode(s2)


class SequenceMatcher:
    def __init__(self, isjunk=None, a='', b='', autojunk=True):
        self.isjunk = isjunk
        self.a = self.b = None
        self.autojunk = autojunk
        self.set_seqs(a, b)

    def set_seqs(self, a, b):
        self.set_seq1(a)
        self.set_seq2(b)

    def set_seq1(self, a):
        if a is self.a:
            return
        self.a = a
        self.matching_blocks = self.opcodes = None

    def set_seq2(self, b):
        if b is self.b:
            return
        self.b = b
        self.matching_blocks = self.opcodes = None
        self.fullbcount = None
        self.__chain_b()

    def __chain_b(self):
        b = self.b
        self.b2j = b2j = {}

        for i, elt in enumerate(b):
            indices = b2j.setdefault(elt, [])
            indices.append(i)
        self.bjunk = junk = set()
        isjunk = self.isjunk
        if isjunk:
            for elt in b2j.keys():
                if isjunk(elt):
                    junk.add(elt)
            for elt in junk:
                del b2j[elt]

        self.bpopular = popular = set()
        n = len(b)
        if self.autojunk and n >= 200:
            ntest = n // 100 + 1
            for elt, idxs in b2j.items():
                if len(idxs) > ntest:
                    popular.add(elt)
            for elt in popular:
                del b2j[elt]

    def ratio(self):
        matches = sum(triple[-1] for triple in self.get_matching_blocks())
        return _calculate_ratio(matches, len(self.a) + len(self.b))

    def get_matching_blocks(self):
        if self.matching_blocks is not None:
            return self.matching_blocks
        la, lb = len(self.a), len(self.b)
        queue = [(0, la, 0, lb)]
        matching_blocks = []
        while queue:
            alo, ahi, blo, bhi = queue.pop()
            i, j, k = x = self.find_longest_match(alo, ahi, blo, bhi)
            if k:
                matching_blocks.append(x)
                if alo < i and blo < j:
                    queue.append((alo, i, blo, j))
                if i+k < ahi and j+k < bhi:
                    queue.append((i+k, ahi, j+k, bhi))
        matching_blocks.sort()

        i1 = j1 = k1 = 0
        non_adjacent = []
        for i2, j2, k2 in matching_blocks:
            if i1 + k1 == i2 and j1 + k1 == j2:
                k1 += k2
            else:
                if k1:
                    non_adjacent.append((i1, j1, k1))
                i1, j1, k1 = i2, j2, k2
        if k1:
            non_adjacent.append((i1, j1, k1))

        non_adjacent.append((la, lb, 0))
        self.matching_blocks = list(map(Match._make, non_adjacent))
        return self.matching_blocks

    def find_longest_match(self, alo=0, ahi=None, blo=0, bhi=None):
        a, b, b2j, isbjunk = self.a, self.b, self.b2j, self.bjunk.__contains__
        if ahi is None:
            ahi = len(a)
        if bhi is None:
            bhi = len(b)
        besti, bestj, bestsize = alo, blo, 0
        j2len = {}
        nothing = []
        for i in range(alo, ahi):
            j2lenget = j2len.get
            newj2len = {}
            for j in b2j.get(a[i], nothing):
                if j < blo:
                    continue
                if j >= bhi:
                    break
                k = newj2len[j] = j2lenget(j-1, 0) + 1
                if k > bestsize:
                    besti, bestj, bestsize = i-k+1, j-k+1, k
            j2len = newj2len
        while besti > alo and bestj > blo and \
                not isbjunk(b[bestj-1]) and \
                a[besti-1] == b[bestj-1]:
            besti, bestj, bestsize = besti-1, bestj-1, bestsize+1
        while besti+bestsize < ahi and bestj+bestsize < bhi and \
                not isbjunk(b[bestj+bestsize]) and \
                a[besti+bestsize] == b[bestj+bestsize]:
            bestsize += 1
        while besti > alo and bestj > blo and \
                isbjunk(b[bestj-1]) and \
                a[besti-1] == b[bestj-1]:
            besti, bestj, bestsize = besti-1, bestj-1, bestsize+1
        while besti+bestsize < ahi and bestj+bestsize < bhi and \
                isbjunk(b[bestj+bestsize]) and \
                a[besti+bestsize] == b[bestj+bestsize]:
            bestsize = bestsize + 1

        return Match(besti, bestj, bestsize)


def _calculate_ratio(matches, length):
    if length:
        return 2.0 * matches / length
    return 1.0


# Match = _namedtuple('Match', 'a b size')


# name = 'Saint Laurent LouLou Top Handle Bag Matelasse Chevron Leather Medium Black'
# val = '%20'.join(name.split(' '))


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

# r = requests.get(
#     f'https://www.vestiairecollective.com/search/?q={val}#sold=1', headers=headers)





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


# while True:
#     try:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         # time.sleep(5)
#         btn = [val for val in driver.find_elements(
#             By.CSS_SELECTOR, 'button') if val.text == 'View more'][0]
#         btn.click()
#         time.sleep(2)
#         # driver.execute_script("arguments[0].click();", btn)
#         # btn.find_element(By.XPATH, '..').click()
#         # print(len(driver.find_elements(By.CSS_SELECTOR, 'a')))
#         # time.sleep(2)
#         # driver.implicitly_wait(1)
#     except IndexError:
#         # links = [val.get_attribute('href') for val in driver.find_elements(By.CSS_SELECTOR, 'a') if '/p/' in val.get_attribute('href')]
#         # Filter out all the products
#         links = [val for val in driver.find_elements(By.CSS_SELECTOR, 'a') if '/p/' in val.get_attribute('href')]
#         # Get only the items that are not sold yet
#         links = [val for val in links if 'SOLD' not in val.text]
#         # 
#         # links = list(itertools.chain.from_iterable([[val.get_attribute('href') for val in links if ele in val.text] for ele in brands]))
#         links = [val.get_attribute('href') for val in links]
#         break


# rows = []
# for link in tqdm(links):
#     driver.get(link)
#     # time.sleep(5)
#     title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[1]/p').text
#     price = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[1]/section/div/div/div/div/div/div/h2').text
#     # description = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[2]/section').text
#     # category = ''
#     # try:
#     #     category = description.split('\n')[description.split('\n').index('Type')+1]
#     # except:
#     #     pass
#     # try:
#     #     brand = description.split('\n')[description.split('\n').index('Brand')+1]
#     # except:
#     #     brand = ''
#     # try:
#     #     condition = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/section/div/div/div').text.split('\nMailing')[0]
#     # except:
#     #     pass
#     text_listing = [val.text for val in driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[2]/section').find_elements(By.CSS_SELECTOR, 'p')]
#     try:
#         brand = text_listing[text_listing.index('Brand')+1]
#     except:
#         brand = ''
#     try:
#         model = text_listing[text_listing.index('Model')+1]
#     except:
#         model = ''
#     try:
#         category = text_listing[text_listing.index('Type')+1]
#     except:
#         category = ''
#     try:
#         accessories = text_listing[text_listing.index('Accessories')+1]
#     except:
#         accessories = ''
#     try:
#         description = text_listing[text_listing.index('Description')+1]
#     except:
#         description = ''
#     try:
#         images = '; '.join([val.get_attribute('src') for val in driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/section/div/div/div').find_elements(By.CSS_SELECTOR, 'img')])
#     except:
#         images = ''
    

#     row = {
#         'title': title,
#         'price': price,
#         'brand': brand,
#         'model': model,
#         'category': category,
#         'accessories': accessories,
#         'description': description,
#         'images': images
#     }

#     rows.append(row)

#     pd.DataFrame(rows).to_csv('/Users/mathieukremeth/Desktop/dcarousell_extract.csv')

#     data = pd.read_csv('/Users/mathieukremeth/Desktop/dcarousell_extract.csv', index_col=0)

#     # Filter by brands
#     data = data[data['brand'].isin(brands)]

#     # Filter by category

#     return data.to_json()


    

# scraper = cloudscraper.create_scraper()
# textt = scraper.get(f'https://www.carousell.sg/u/diamondquilting/').text
# driver.maximize_window()
# driver.implicitly_wait(10)
# driver.delete_all_cookies()


# tt = scraper.get(
#     f'https://www.vestiairecollective.com/search/?q={val}#sold=1').text.split('catalog__flexContainer')
# tt = [val for val in tt if '--item--withFilters' and 'handbags' in val]

# ddd = []
# for i, v in enumerate(tt):
#     brand = v.split('"productSnippet__brand">')[-1].split('</span>')[0]
#     if brand[-1] == ' ':
#         brand = brand[:-1]

#     title = v.split('"productSnippet__name">')[-1].split('</span>')[0]
#     if title[-1] == ' ':
#         title = title[:-1]
#     price_split = v.split('$')
#     if len(price_split) == 3:
#         price = price_split[1].split('<span')[0]

#     elif len(price_split) == 4:
#         price = price_split[2].split('<span')[0]

#     else:
#         continue

#     if price[-1] == ' ':
#         price = price[:-1]

#     ddd.append([brand + ' ' + title, price])

# names_only = [val[0] for val in ddd]

# dd = {}
# for val in names_only:
#     dd[val] = token_set_ratio(name, val)

# get_price = ddd[[val[0] for val in ddd].index(
#     sorted(dd, key=dd.get, reverse=True)[0])][1]


if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()



