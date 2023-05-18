# @ Load the package


# @ Driver
from tool.DownloadUtil import *
from service.GUService import *

DRIVER_PATH = './chromedriver'
# options = Options()
# options.headless = True
# options.add_argument("--window-size=1920,1200")
# chromedriver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
# chromedriver = webdriver.Chrome(executable_path=DRIVER_PATH)

# GU DIR
GUDIR = 'gu'
UQDIR = 'uq'

downloadUtil = DownloadUtil()
gUService = GUService()


class WebCrawlerService():

    def webCraw(self, webType):
        if webType == "GU":
            downloadUtil.createOrDelDir(GUDIR)
            return self.GUstart()
        elif webType == "UQ":
            return 2

    def GUstart(self):

        womenUrl = 'https://www.gu-global.com/tw/zh_TW/L1_women.html'
        menUrl = 'https://www.gu-global.com/tw/zh_TW/L1_men.html'
        kidUrl = 'https://www.gu-global.com/tw/zh_TW/L1_kids.html'
        genderList = [womenUrl, menUrl, kidUrl]
        guList = [{"gender": 'womenUrl', "url": womenUrl},
                  {"gender": 'menUrl', "url": menUrl},
                  {"gender": 'kidUrl', "url": kidUrl}]

        for i in guList:
            # 1
            print(i.get("gender"))
            gUService.listGenderCategory(i.get("url"))
            # genderCategoryProductList = self.listGenderCategory(i)
            # if len(genderCategoryProductList) > 0:
            #     for url in genderCategoryProductList:
            #         self.listProductCode(url)
            # genderCategoryProductList.clear()
        gUService.closeDriver()
