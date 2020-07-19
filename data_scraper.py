from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')


class DataScraper:
    # TODO: MANY THINGS
    def __init__(self):
        self.driver = webdriver.Chrome('./Utils/chromedriver', options=options)

    def read_page(self):
        soup = BeautifulSoup(self.driver.current_url)
        print(soup.find_all("div"))
