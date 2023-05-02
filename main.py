# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup

# @ Load the package

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
import urllib
# from sqlalchemy import create_engine
import random


# @ Driver
DRIVER_PATH = './chromedriver'
# options = Options()
# options.headless = True
# options.add_argument("--window-size=1920,1200")
# chromedriver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
chromedriver = webdriver.Chrome(executable_path=DRIVER_PATH)


# 設置 Chrome 瀏覽器
driver = webdriver.Chrome()

# 設置等待時間
wait = WebDriverWait(driver, 10)

# 前往GU網站
driver.get('https://www.gu-global.com/tw/zh_TW/women_printT.html')

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def listDetail():
    try:
        r = requests.get("https://www.gu-global.com/tw/zh_TW/product-detail.html?productCode=u0000000008190")
        soup = BeautifulSoup(r.text, "html.parser")
        print(soup.prettify())
        detailWeb = chromedriver.get("https://www.gu-global.com/tw/zh_TW/product-detail.html?productCode=u0000000008190")
        detailDiv = chromedriver.find_element(By.CLASS_NAME,'h-col.gu-product-detail-list')
        # 產品名稱
        detailTitle = chromedriver.find_element(By.CLASS_NAME,'gu-product-detail-list-title').text
        # 產品價錢
        picEle = chromedriver.find_element(By.CLASS_NAME,'detail-list-price-main').text
        imgFile = chromedriver.find_element(By.CLASS_NAME,'detail-img')
        pc = None

    except Exception as e:
        print(e)


def listProductCode():
    try:
        productListWeb = chromedriver.get("https://www.gu-global.com/tw/zh_TW/women_jacket.html")
        # products = wait.until(chromedriver.presence_of_all_elements_located((By.CSS_SELECTOR, '.product-item__body')))
        productList = []
        dict = {}
        productList1 = chromedriver.find_elements(By.CLASS_NAME,'product-li')
        for product in productList1:
            productUrl = product.find_element(By.CSS_SELECTOR,'a.product-herf')
            url = productUrl.get_attribute('href')
            productText = product.text
            if(productText.count('\n')==1):
                productName,productPrice = productText.split('\n')
            else:
                productName,productPrice,text = productText.split('\n')
            print(productName+'and price is :'+productPrice)
            productList.append({"productName":productName,"productPrice":productPrice,"Url":url})

        # print(productList)
        print(123)
    except Exception as e:
        print(e)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startTime = time.time()
    print("try to get web")
    # web = None
    listDetail()
    listProductCode()

    try:
        web = chromedriver.get("https://www.gu-global.com/tw/zh_TW/L1_women.html")
        # //*[@id="hmall-container"]/div/div[1]/div[1]/div/div/header/div/div[2]/ul/li[2]/a
        # //*[@id="hmall-container"]/div/div[1]/div[3]/div/div/div[3]/ul/li

        # /html/body/div[2]/div/div[1]/div[3]/div/div/div[1]/div/div/a[2]
        # // *[ @ id = "hmall-container"] / div / div[1] / div[3] / div / div / div[2] / div[3] / ul / li[1] / a / img
    except Exception as e:
        print(e)

    try:
        1
        # list = chromedriver.find_element(By.XPATH,'// *[ @ id = "hmall-container"] / div / div[1] / div[3] / div / div / div[2] / div[3] / ul ')
        # list = chromedriver.find_elements(By.ID,"bd_categories")
        # items = list.find_elements(By.TAG_NAME,'li')
        # for l in list:
        #     print(l.get_attribute(href))

    except Exception as e:
        print(e)


    # soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify())
    # hmall = soup.findAll("div", {"id": "hmall-container"})
    # print(hmall[0])
    # selected = hmall

    for s in selected:
        print(s["href"], s.text)
    # print(r.text)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
