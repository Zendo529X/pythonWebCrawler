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
DRIVER_PATH = './chromedriver'
# options = Options()
# options.headless = True
# options.add_argument("--window-size=1920,1200")
# chromedriver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
chromedriver = webdriver.Chrome(executable_path=DRIVER_PATH)

# GU DIR
GUDIR = 'gu'
UQDIR = 'uq'


class WebCrawlerService():

    def webCraw(self, webType):
        if webType == "GU":
            return 1
        elif webType == "UQ":
            return 2
