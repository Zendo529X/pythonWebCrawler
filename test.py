from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 設置 Chrome 瀏覽器
driver = webdriver.Chrome()

# 設置等待時間
wait = WebDriverWait(driver, 10)

# 前往GU網站
driver.get('https://www.gu-global.com/tw/zh_TW/women_printT.html')

# 找到所有產品
products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.product-item__body')))

# 逐一爬取產品資訊
for product in products:
    # 找到產品名稱
    name = product.find_element(By.CSS_SELECTOR, '.product-item__name').text

    # 找到產品價格
    price = product.find_element(By.CSS_SELECTOR, '.product-item__price').text

    # 找到產品圖片連結
    image = product.find_element(By.CSS_SELECTOR, '.product-item__image img').get_attribute('src')

    # 找到產品網址
    url = product.find_element(By.CSS_SELECTOR, '.product-item__link').get_attribute('href')

    # 顯示產品資訊
    print(name, price, image, url)

# 關閉瀏覽器
driver.quit()
