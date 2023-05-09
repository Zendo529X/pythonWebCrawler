# @ Load the package

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import dateutil.relativedelta
import pandas as pd
import os
import sys
import urllib.request
import random
import shutil
import pyautogui

# @ Driver
from tool.DownloadUtil import *

DRIVER_PATH = './chromedriver'
options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.headless = True
options.add_argument("--window-size=1920,1200")
chromedriver = webdriver.Chrome(executable_path=DRIVER_PATH,options=options)
# chromedriver = webdriver.Chrome(executable_path=DRIVER_PATH)

# GU DIR
GUDIR = 'gu'
UQDIR = 'uq'

downloadUtil = DownloadUtil()


class GUService():
    def closeDriver(self):
        chromedriver.close()

    def listGenderCategory(self, genderUrl):
        print(genderUrl)
        try:
            chromedriver.get(genderUrl)
            categoryLists = chromedriver.find_elements(By.CLASS_NAME, 'bd_categories_item')
        except Exception as e:
            print(e)
        categoryUrlList = []
        try:
            for category in categoryLists:
                categoryItem = category.find_element(By.TAG_NAME, 'a')
                categoryUrl = categoryItem.get_attribute('href')
                print(categoryUrl)
                categoryUrlList.append(categoryUrl)
        except Exception as e:
            print(e)

        if len(categoryUrlList) > 0:
            for url in categoryUrlList:
                self.listProductCode(url)

        # return categoryUrlList

    def listProductCode(self, url):
        print(url)
        try:
            # productListWeb = chromedriver.get('https://www.gu-global.com/tw/zh_TW/women_jacket.html')
            productListWeb = chromedriver.get(url)
            time.sleep(3)
            # products = wait.until(chromedriver.presence_of_all_elements_located((By.CSS_SELECTOR, '.product-item__body')))
            productList = []
            dict = {}
            productList1 = chromedriver.find_elements(By.CLASS_NAME, 'product-li')
            for product in productList1:
                productUrl = product.find_element(By.CSS_SELECTOR, 'a.product-herf')
                url = productUrl.get_attribute('href')
                productText = product.text
                # downPic(url)

                if (productText.count('\n') == 1):
                    productName, productPrice = productText.split('\n')
                else:
                    productName, productPrice, text = productText.split('\n')
                print(productName + 'and price is :' + productPrice)
                productList.append({"productName": productName, "productPrice": productPrice, "url": url})

            # 先加入list後 再進行撈圖
            for prod in productList:
                self.downPic(prod.get("url"))

            # print(productList)
            # chromedriver.back()
            # chromedriver.close()
            print(123)
        except Exception as e:
            print(e)

    def downPic(self, url):
        try:
            print(url)
            # chromedriver.switch_to.window(chromedriver.window_handles[1])
            detailWeb = chromedriver.get(url)
            time.sleep(2)
            productTitle = chromedriver.find_element(By.CLASS_NAME, 'gu-product-detail-list-title').text
            downloadUtil.createOrDelDir(GUDIR)
            productTitle = GUDIR + '/' + productTitle
            downloadUtil.createOrDelDir(productTitle)

            productImgListUl = chromedriver.find_elements(By.CLASS_NAME, 'sku-li')
            productCode = ''
            fileName = ''
            for li in productImgListUl:
                imgUrl = li.find_element(By.CSS_SELECTOR, 'img.sku-img')
                img = imgUrl.get_attribute('src')
                fileName = img.split('/')[-1]
                productCode = img.split('test/')[1].split('/')[0]
                fileName = productTitle + '/' + productCode + '_' + fileName

                # urllib.request.urlretrieve(img,productTitle+'.png')
                urllib.request.urlretrieve(img, fileName)

            # chromedriver.back()

        except Exception as e:
            print(e)
