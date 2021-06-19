import scrapy
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.selector import Selector
from selenium.webdriver.support import expected_conditions as EC



class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['livecoinwatch.com']
    start_urls=["https://www.livecoinwatch.com"]

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)
        driver.set_window_size(1920,1080)
        driver.get("https://www.livecoinwatch.com")
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//div[@class="dropdown-content currency-selector-content"]/div[2]/div/div[2]/button')))
        driver.execute_script("arguments[0].click();", element)
        element1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//div[@class="d-md-inline-flex d-none pagination-per-page"]/div/div/div[@class="dropdown-content"]/button[4]')))
        driver.execute_script("arguments[0].click();", element1)
        
        self.html=driver.page_source
        driver.close()
    def parse(self, response):
        res=Selector(text=self.html)
        for coins in res.xpath('//tbody/tr[@class="table-row filter-row"]'):
            coin= coins.xpath('.//td[2]/a/div/div[2]/div/text()').get()
            price_EUR=coins.xpath('.//td[3]/text()[2]').get()
            yield{
                'Coin':coin,
                'EUR':price_EUR
            }
       
        
          

            
 