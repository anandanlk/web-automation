from selenium import webdriver
from config import manifest


class SeleniumInterface:
    def __init__(self):
        self.browser = webdriver.Chrome()
        pass

    def open_browser(self):
        if self.browser == 'chrome':
            self.browser = webdriver.Chrome()

    def navigate(self, url):
        self.browser.get(url)
