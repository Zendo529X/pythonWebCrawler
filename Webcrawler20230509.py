#@Reference
#https://www.scrapingbee.com/blog/selenium-python/
#https://selenium-python.readthedocs.io/locating-elements.html
#https://www.browserstack.com/guide/python-selenium-select-dropdown


#@ Load the package
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



#@ Driver
#https://sites.google.com/chromium.org/driver/downloads
DRIVER_PATH = './chromedriver'
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
chromedriver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
#driver = webdriver.Chrome(executable_path=DRIVER_PATH)


#@ Initial Information

##@ Website
SearchWeb = 'https://unipass.customs.go.kr/ets/index_eng.do'

##@ Time
periodtype = 'Month' #Period Type
date_today = datetime.now().strftime("%Y.%m.%d")  # Today
date_from = datetime.now() + dateutil.relativedelta.relativedelta(months=-3)
periodfrom = date_from.strftime("%Y.%m")  # Period From
#periodfrom = "2021.08"  # Period From
date_to = datetime.now() + dateutil.relativedelta.relativedelta(months=-2)
periodto = date_to.strftime("%Y.%m")  # Period To
#periodto = "2023.03"  # Period To

##@ Product Code
productcode = ['290220', '290250', '290243', '290241', '290230', '291736', '270730']
#productcode = ['290220']

##@ Set up Dataframe
importexportinfo = []

##@ SQL Information
#Driver: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16
sqldriver='ODBC Driver 18 for SQL Server'
server_name= 'ilingprojecttest.database.windows.net'
db='projectdb'
uid='iling11009052'
pwd='ILing820816*'





def OpenWebsite(weburl):
    try:
        chromedriver.get(weburl)
        print("Current URL:"+chromedriver.current_url)
    except Exception as e:
        print('捕捉錯誤資訊: ', e)

def ClickButton(buttontype, buttonxpath):
    try:
        buttonarea = chromedriver.find_element(buttontype, buttonxpath)
        print("Press the Button: "+buttonarea.text)
        buttonarea.click()
        time.sleep(random.randint(1,4))
    except Exception as e:
        print('捕捉錯誤資訊: ', e)

def SelectOption(optionxpath, filloption):
    try:
        fillarea = chromedriver.find_element(By.XPATH, optionxpath)
        dropoption = Select(fillarea)
        dropoption.select_by_visible_text(filloption)
        selected_option = dropoption.first_selected_option.text
        print ("Select Option: "+selected_option)
    except Exception as e:
        print('捕捉錯誤資訊: ', e)

def FillText(textxpath, textcontent):
    try:
        fillarea = chromedriver.find_element(By.XPATH, textxpath)
        fillarea.send_keys(textcontent)
        print ("Fill Text: "+fillarea.get_attribute('value'))
    except Exception as e:
        print('捕捉錯誤資訊: ', e)

def FindInfo(infoxpath):
    try:
        infoarea = chromedriver.find_element(By.XPATH, infoxpath)
        print("Info: ", infoarea.text)
    except Exception as e:
        print('捕捉錯誤資訊: ', e)

def GetTableInfo():
    tableinformation = chromedriver.find_elements(By.XPATH, '//*[@id="TRS0104024Q_table"]/tbody/tr')
    for row in tableinformation:
        rowinfo = []
        tablecol = row.find_elements(By.TAG_NAME, "td")
        for col in tablecol:
            rowinfo.append(col.text)
        importexportinfo.append(rowinfo)








if __name__ == '__main__':
    for code in productcode:
        #@ Open Website
        OpenWebsite(SearchWeb)
        #@ Click and to another page
        ClickButton(By.XPATH, '//*[@id="maincont"]/div/article/ul/li[4]/a')
        #@ Fill the Form -- Select Period
        SelectOption('//*[@id="TRS0104024Q_priodKind"]', periodtype)
        SelectOption('//*[@id="TRS0104024Q_priodFr"]', periodfrom)
        SelectOption('//*[@id="TRS0104024Q_priodTo"]', periodto)
        #@ Fill the Form -- Input Code
        print("Product Code:"+code)
        FillText('//*[@id="TRS0104024Q_hsSgn02"]', code[0:2])
        FillText('//*[@id="TRS0104024Q_hsSgn04"]', code[2:4])
        FillText('//*[@id="TRS0104024Q_hsSgn06"]', code[4:])
        #@ Fill the Form -- Select Country
        SelectOption('//*[@id="TRS0104024Q_cntyCd"]', '-- Select--')
        #@ Fill the Form -- Submit
        ClickButton(By.XPATH, '//*[@id="TRS0104024Q_fmSearch"]/div/footer/button')
        #@ Choose per Page -- Find the Row Numbers
        FindInfo('//*[@id="TRS0104024Q_tab1"]/div/aside/div[1]/span[1]/strong')
        #@ Choose per Page -- Select 100
        SelectOption('//*[@id="TRS0104024Q_tab1"]/div/aside/div[1]/span[2]/select', '100')
        #@ Choose per Page -- Submit
        ClickButton(By.XPATH, '//*[@id="TRS0104024Q_tab1"]/div/aside/div[1]/span[2]/button')
        #@ Get the Information -- Page Number
        nowpage = chromedriver.find_elements(By.XPATH, '//*[@id="TRS0104024Q_tab1"]/div/div[2]/ul/li')
        for p in nowpage:
            if p.get_attribute('class')=='selected':
                print(p.find_element(By.TAG_NAME, 'strong').text)
                #@ Get the Information -- Get Table
                GetTableInfo()
            else:
                ClickButton(By.TAG_NAME, 'a')
                #@ Get the Information -- Get Table
                GetTableInfo()
    
    chromedriver.quit()
    
    # #@ Get the Information -- Country Transfer
    # importexportdf = pd.DataFrame(importexportinfo, columns=['Input', 'Period', 'CountryEnglish', 'Items', 'HSCode', 'ExportWeight', 'ExportValue', 'ImportWeight', 'ImportValue', 'BalanceofTrade'])
    # rslt_df = importexportdf[importexportdf['Period'] != "Total"].drop('Input', axis=1)
    # coutrytranfer = pd.read_excel('18054627213697_CountryTranslate.xlsx', usecols=['English_Name', 'Chinese_Name'])
    # importexportdffinal = pd.merge(rslt_df, coutrytranfer, left_on="CountryEnglish", right_on="English_Name")
    # importexportdffinal = importexportdffinal.rename(columns={"Chinese_Name": "CountryChinese"})
    # importexportdffinal = importexportdffinal.drop('English_Name', axis=1)
    #
    #
    # #@ Save to Excel
    # print("Save to Excel...")
    # importexportdffinal.to_excel(f"HS CODE by Country_{date_today}.xlsx", index=False)
    #
    # #@ Save to the SQL
    # print("Save to Sql...")
    # params_jyt=urllib.parse.quote_plus(f"Driver={{{sqldriver}}};Server=tcp:{server_name},1433;Database={db};Uid={uid};Pwd={pwd}")
    # # engine_db=create_engine(f"mssql+pyodbc:///?odbc_connect={params_jyt}",fast_executemany=True)
    # # importexportdffinal.to_sql("hscodebycountry",engine_db, index=False,if_exists='append')