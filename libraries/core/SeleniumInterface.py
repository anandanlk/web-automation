import json
import os
import sys

from selenium import webdriver
from config import manifest


class SeleniumInterface:
    def __init__(self):
        self.browser = manifest.browser
        self.page_load_timeout = manifest.page_load_timeout
        self.script_timeout = manifest.script_timeout
        self.project_dir = os.getcwd()
        with open(os.path.join(self.project_dir, "object_repository", manifest.object_repository)) as f:
            self.objects = json.load(f)

    def open_browser(self):
        if self.browser == 'chrome':
            self.browser = webdriver.Chrome()
        else:
            raise AssertionError(f'Browser {self.browser} is not supported')

    def navigate(self, page):
        self.browser.get(manifest.base_url/self.objects[page]["path"])
