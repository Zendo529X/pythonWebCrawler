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
DRIVER_PATH = './chromedriver'
# options = Options()
# options.headless = True
# options.add_argument("--window-size=1920,1200")
# chromedriver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
chromedriver = webdriver.Chrome(executable_path=DRIVER_PATH)


#@ Initial Information

##@ Time
periodtype = 'Month' #Period Type
date_today = datetime.now().strftime("%Y.%m.%d")  # Today
date_from = datetime.now() + dateutil.relativedelta.relativedelta(months=-2)
periodfrom = date_from.strftime("%Y.%m")  # Period From
date_to = datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
periodto = date_to.strftime("%Y.%m")  # Period To

##@ Product Code
productcode = ['290220', '290250', '290243', '290241', '290230', '291736', '270730']
#productcode = ['290220']

##@ Set up Dataframe
importexportinfo = []

##@ SQL Information
sqldriver='ODBC Driver 18 for SQL Server'
server_name= 'ilingprojecttest.database.windows.net'
db='projectdb'
uid='iling11009052'
pwd='ILing820816*'



for code in productcode:
    print("Product Code:"+code)

    #@ Open Website
    try:
        # chromedriver.get('https://unipass.customs.go.kr/ets/index_eng.do')
        chromedriver.get('https://www.uniqlo.com/tw/zh_TW/')
        print("Current URL:"+chromedriver.current_url)
    except Exception as e:
        print('捕捉錯誤資訊: '+ str(e))
        break

    #@ Click and to another page
    try:
        h1 = chromedriver.find_element(By.XPA, '//*[@id="maincont"]/div/article/ul/li[4]/a')
        print("Change to another page:"+h1.text)
        h1.click()
        time.sleep(random.randint(1,4))
    except Exception as e:
        print('捕捉錯誤資訊: '+ str(e))
        break

    #@ Fill the Form -- Select Period
    try:
        fillperiod = chromedriver.find_element(By.XPATH, '//*[@id="TRS0104024Q_priodKind"]')
        drpperiodtype = Select(fillperiod)
        drpperiodtype.select_by_visible_text(periodtype)
        selected_option = drpperiodtype.first_selected_option.text
        print ("Select Period Type:"+selected_option)

        fillperiodfrom = chromedriver.find_element(By.XPATH, '//*[@id="TRS0104024Q_priodFr"]')
        drpperiodfrom = Select(fillperiodfrom)
        drpperiodfrom.select_by_visible_text(periodfrom)
        selected_option = drpperiodfrom.first_selected_option.text
        print ("Select Period Start:"+selected_option)

        fillperiodto = chromedriver.find_element(By.XPATH, '//*[@id="TRS0104024Q_priodTo"]')
        drpperiodto = Select(fillperiodto)
        drpperiodto.select_by_visible_text(periodto)
        selected_option = drpperiodto.first_selected_option.text
        print ("Select Period End:"+selected_option)
        time.sleep(2)
    except Exception as e:
        print('捕捉錯誤資訊: '+ str(e))
        break

    #@ Fill the Form -- Input Code
    try:
        fillcode = chromedriver.find_element(By.XPATH, '//*[@id="TRS0104024Q_hsSgn02"]')
        fillcode.send_keys(code[0:2])
        fillcode1 = chromedriver.find_element(By.XPATH, '//*[@id="TRS0104024Q_hsSgn04"]')
        fillcode1.send_keys(code[2:4])
        fillcode2 = chromedriver.find_element(By.XPATH, '//*[@id="TRS0104024Q_hsSgn06"]')
        fillcode2.send_keys(code[4:])
        print ("Code:"+fillcode.get_attribute('value')+fillcode1.get_attribute('value')+"."+fillcode2.get_attribute('value'))
    except Exception as e:
        print('捕捉錯誤資訊: '+ str(e))
        break

    #@ Select Country
    try:
        fillcountry = chromedriver.find_element(By.XPATH, '//*[@id="TRS0104024Q_cntyCd"]')
        drpcountry = Select(fillcountry)
        #for opt in drpcountry.options:
        #    print(opt.text)
        drpcountry.select_by_visible_text('-- Select--')
        selected_option = drpcountry.first_selected_option.text
        print ("Select Country:"+selected_option)
        time.sleep(2)
    except Exception as e:
        print('捕捉錯誤資訊: '+ str(e))
        break


    #@ Fill the Form -- Submit
    try:
        inquery = chromedriver.find_element(By.XPATH, '//*[@id="TRS0104024Q_fmSearch"]/div/footer/button')
        print("Press the Button:"+inquery.text)
        inquery.click()
        time.sleep(2)
    except Exception as e:
        print(e)
        print('捕捉錯誤資訊: '+ str(e))
        break


    #@ Get Information
    try:
        ##@ Row Numbers
        ItemNo = chromedriver.find_element(By.XPATH, '//*[@id="TRS0104024Q_tab1"]/div/aside/div[1]/span[1]/strong')
        rownum = int(ItemNo.text)
        print("The Number of Column: ", rownum)

        ##@ Chose per Page to 100
        Choseperpage = chromedriver.find_element(By.XPATH, '//*[@id="TRS0104024Q_tab1"]/div/aside/div[1]/span[2]/select')
        drprow = Select(Choseperpage)
        drprow.select_by_visible_text('100')
        selected_row = drprow.first_selected_option.text
        print ("Select Row:"+selected_row)
        time.sleep(2)

        submitbutton = chromedriver.find_element(By.XPATH, '//*[@id="TRS0104024Q_tab1"]/div/aside/div[1]/span[2]/button')
        print("Press the Button:"+submitbutton.text)
        submitbutton.click()
        time.sleep(2)

        ##@ Get the row information
        nowpage = chromedriver.find_elements(By.XPATH, '//*[@id="TRS0104024Q_tab1"]/div/div[2]/ul/li')
        i = 1

        for p in nowpage:
            pi = int(p.text)
            if i == pi:
                tableinformation = chromedriver.find_elements(By.XPATH, '//*[@id="TRS0104024Q_table"]/tbody/tr')
                for row in range(2,len(tableinformation)+1):
                    rowinfo = []
                    tablecol = chromedriver.find_elements(By.XPATH, f"//*[@id='TRS0104024Q_table']/tbody/tr[{row}]/td")
                    for col in range(2, len(tablecol)+1):
                        info = chromedriver.find_element(By.XPATH, f"//*[@id='TRS0104024Q_table']/tbody/tr[{row}]/td[{col}]")
                        rowinfo.append(info.text)
                        print("info: "+ info.text)
                    importexportinfo.append(rowinfo)
            else:
                pagebutton = chromedriver.find_element(By.XPATH, f'//*[@id="TRS0104024Q_tab1"]/div/div[2]/ul/li[{p.text}]/a')
                print("Press the Button:"+pagebutton.text)
                pagebutton.click()
                time.sleep(2)
                i = int(pi)

                tableinformation = chromedriver.find_elements(By.XPATH, '//*[@id="TRS0104024Q_table"]/tbody/tr')
                for row in range(1,len(tableinformation)+1):
                    rowinfo = []
                    tablecol = chromedriver.find_elements(By.XPATH, f"//*[@id='TRS0104024Q_table']/tbody/tr[{row}]/td")
                    for col in range(2, len(tablecol)+1):
                        info = chromedriver.find_element(By.XPATH, f"//*[@id='TRS0104024Q_table']/tbody/tr[{row}]/td[{col}]")
                        rowinfo.append(info.text)
                        print("info: "+ info.text)
                    importexportinfo.append(rowinfo)

    except Exception as e:
        print('捕捉錯誤資訊: '+ str(e))
        break

chromedriver.quit()

#@ Save to Excel
print("Save to Excel...")
importexportdf = pd.DataFrame(importexportinfo, columns=['Period', 'Country', 'Items', 'HSCode', 'ExportWeight', 'ExportValue', 'ImportWeight', 'ImportValue', 'BalanceofTrade'])
importexportdf.to_excel(f"HS CODE by Country_{date_today}.xlsx", index=False)

#@ Save to the SQL
print("Save to Sql...")
params_jyt=urllib.parse.quote_plus(f"Driver={{{sqldriver}}};Server=tcp:{server_name},1433;Database={db};Uid={uid};Pwd={pwd}")
engine_db=create_engine(f"mssql+pyodbc:///?odbc_connect={params_jyt}",fast_executemany=True)
importexportdf.to_sql("hscodebycountry",engine_db, index=False,if_exists='append')
