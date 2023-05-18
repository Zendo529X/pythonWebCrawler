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
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
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

# for Chrome
# DRIVER_PATH = './chromedriver'
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.headless = True
# options.add_argument("--window-size=1920,1200")
# driver = webdriver.Chrome(executable_path=DRIVER_PATH,options=options)
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)


# for FireFox
DRIVER_PATH = './geckodriver'
firefox_binary = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.headless = True
# options.add_argument("--window-size=1920,1200")
driver = webdriver.Firefox(executable_path=DRIVER_PATH, options=options, firefox_binary=firefox_binary)
# driver = webdriver.Firefox(executable_path=DRIVER_PATH)


wait = WebDriverWait(driver, 10)

# GU DIR
GUDIR = 'gu'
UQDIR = 'uq'

downloadUtil = DownloadUtil()


class GUService():

    def closeDriver(self):
        if (driver != None):
            driver.quit()

    def listGenderCategory(self, genderUrl):
        print("====== start list category ======")
        print(genderUrl)
        try:
            driver.get(genderUrl)
            categoryListstitle = wait.until(EC.visibility_of(driver.find_element(By.CLASS_NAME, "h2_subject")))
            categoryLists = driver.find_elements(By.CLASS_NAME, 'bd_categories_item')
            # self.closeDriver()
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

        print("====== start list product ======")

        if len(categoryUrlList) > 0:
            for url in categoryUrlList:
                self.listProductCode(url)

        # return categoryUrlList
        self.closeDriver()

    def listProductCode(self, url):
        print("====== try to get product ======")
        print(url)
        try:
            # productListWeb = driver.get('https://www.gu-global.com/tw/zh_TW/women_jacket.html')
            productListWeb = driver.get(url)
            time.sleep(3)
            # products = wait.until(driver.presence_of_all_elements_located((By.CSS_SELECTOR, '.product-item__body')))
            productList = []
            dict = {}
            listTitle = wait.until(EC.visibility_of(driver.find_element(By.CLASS_NAME, 'mainTitle')))
            groupProductUl = driver.find_elements(By.CLASS_NAME, 'product-ul')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            for groupProduct in groupProductUl:
                productListli = groupProduct.find_elements(By.CLASS_NAME, 'product-li')

                for product in productListli:
                    # time.sleep(1)
                    if (product.tag_name == 'li'):
                        divInA = product.find_element(By.CLASS_NAME,'product-content')
                        tagList = divInA.find_elements(By.TAG_NAME,'div')
                        productName = product.find_element(By.CLASS_NAME, 'font-p-gu').text
                        productUrl = product.find_element(By.CSS_SELECTOR, 'a.product-herf')
                        url = productUrl.get_attribute('href')
                        innerH = product.get_attribute('innerHTML')
                        outerH = product.get_attribute('outerHTML')


                        ######     one way
                        if 'product-price' in outerH:
                            # productPrice = product.find_element(By.CLASS_NAME,'product-price').text
                            productPrice = product.find_element(By.CSS_SELECTOR,'div.product-price').text
                        else:
                            # productPrice = product.find_element(By.CLASS_NAME,'sold-out').text
                            productPrice = product.find_element(By.CSS_SELECTOR,'div.sold-out').text

                        ######     another
                        # productPrice = product.find_element(By.CLASS_NAME,'product-price').text \
                        #     if 'product-price' in outerH \
                        #     else product.find_element(By.CLASS_NAME, 'sold-out').text

                        ######      three way
                        # productPrice = (product.find_element(By.CLASS_NAME,'sold-out'), product.find_element(By.CLASS_NAME,'product-price'))['product-price' in outerH]


                        print(productName + ' and price is : ' + productPrice)
                        productList.append({"productName": productName, "productPrice": productPrice, "url": url})

            # 先加入list後 再進行撈圖
            for prod in productList:
                self.downPic(prod.get("url"))

            print("====== this category of gender is done ======")
        except Exception as e:
            print(e)

    def downPic(self, url):
        try:
            print("====== try to get pic of product ======")
            print(url)
            # driver.switch_to.window(driver.window_handles[1])
            detailWeb = driver.get(url)
            time.sleep(2)
            tempTitle = wait.until(EC.visibility_of(driver.find_element(By.CLASS_NAME, 'gu-product-detail-list-title')))
            # time.sleep(2)
            productTitle = driver.find_element(By.CLASS_NAME, 'gu-product-detail-list-title').text
            # downloadUtil.createOrDelDir(GUDIR)
            productTitle = GUDIR + '/' + productTitle
            downloadUtil.createOrDelDir(productTitle)

            productImgListUl = driver.find_elements(By.CLASS_NAME, 'sku-li')
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

            print("====== this pic of product is done ======")

        except Exception as e:
            print(e)
