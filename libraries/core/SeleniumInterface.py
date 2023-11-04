import json
import os
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from config import manifest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class SeleniumInterface:
    def __init__(self):
        self.browser = manifest.browser
        self.page_load_timeout = manifest.page_load_timeout
        self.timeout = manifest.timeout
        self.project_dir = os.getcwd()
        self.page = ""
        self.action = None
        with open(os.path.join(self.project_dir, "object_repository", manifest.object_repository)) as f:
            self.OR = json.load(f)

    def open_browser(self):
        if self.browser == 'chrome':
            self.browser = webdriver.Chrome()
        else:
            raise AssertionError(f"Browser {self.browser} is not supported")
        self.action = ActionChains(self.browser)

    def navigate(self, page):
        try:
            self.browser.get(manifest.base_url / self.OR[page]["path"])
            self.page = page
        except Exception as e:
            raise AssertionError(f"def:navigate - Unable to navigate to page  -> {e}")

    def switch_to_frame(self, frame):
        try:
            print(f"def:switch_to_frame() - Trying to switch to frame {frame}")
            # self.browser.switch_to.frame(frame)
            WebDriverWait(self.browser, 30).until(ec.frame_to_be_available_and_switch_to_it((By.NAME, frame)))
            print(f"def:switch_to_frame() - Successfully switched to frame {frame}")
        except Exception as e:
            raise AssertionError(f"def:switch_to_frame - Unable to switch to frame  -> {e}")

    def ews_scroll_to_view(self, element_key):
        try:
            print(f"Scrolling up to {element_key}")
            _element = self.find_web_element(element_key)
            self.browser.execute_script("arguments[0].scrollIntoView();", _element)
            print(f"Successfully scrolled up to {element_key}")
        except Exception as e:
            raise AssertionError(f"def:scroll_to_view() - Unable to scroll down -> {e}")

    def find_web_element(self, element_key):
        try:
            _element = None
            match self.OR[self.page][element_key]["locator"]:
                case "id":
                    _element = By.ID, self.OR[self.page][element_key]["value"]
                case "name":
                    _element = By.NAME, self.OR[self.page][element_key]["value"]
                case "xpath":
                    _element = By.XPATH, self.OR[self.page][element_key]["value"]
                case "link_text":
                    _element = By.LINK_TEXT, self.OR[self.page][element_key]["value"]
                case "partial_link_text":
                    _element = By.PARTIAL_LINK_TEXT, self.OR[self.page][element_key]["value"]
                case "tag_name":
                    _element = By.TAG_NAME, self.OR[self.page][element_key]["value"]
                case "class_name":
                    _element = By.CLASS_NAME, self.OR[self.page][element_key]["value"]
                case "css_selector":
                    _element = By.CSS_SELECTOR, self.OR[self.page][element_key]["value"]
                case _:
                    raise "Element not found in the object repository"
            return WebDriverWait(self.browser, self.timeout).until(ec.presence_of_element_located(_element))
        except Exception as e:
            raise AssertionError(f"def:find_web_element -> Unable to find web element - Error : {e}")

    def find_element(self, element_key):
        try:
            match self.OR[self.page][element_key]["locator"]:
                case "id":
                    return By.ID, self.OR[self.page][element_key]["value"]
                case "name":
                    return By.NAME, self.OR[self.page][element_key]["value"]
                case "xpath":
                    return By.XPATH, self.OR[self.page][element_key]["value"]
                case "link_text":
                    return By.LINK_TEXT, self.OR[self.page][element_key]["value"]
                case "partial_link_text":
                    return By.PARTIAL_LINK_TEXT, self.OR[self.page][element_key]["value"]
                case "tag_name":
                    return By.TAG_NAME, self.OR[self.page][element_key]["value"]
                case "class_name":
                    return By.CLASS_NAME, self.OR[self.page][element_key]["value"]
                case "css_selector":
                    return By.CSS_SELECTOR, self.OR[self.page][element_key]["value"]
                case _:
                    raise "Element not found in the object repository"
        except Exception as e:
            raise AssertionError(f"def:find_element -> Unable to find element - Error : {e}")

    def click_alert_ok(self):
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
        except Exception as e:
            raise AssertionError(f"def:click_alert_ok -> Unable to Click the button - Error : {e}")

    def check_alert_status(self):
        try:
            print("Checking the alert status")
            _element = WebDriverWait(self.browser, self.timeout).until(ec.alert_is_present())
            print(_element)
            if _element:
                print("Alert successfully found")
                return True
            else:
                print("Alert not found")
                return False
        except Exception as e:
            print(f"Alert not found: {e}")
            return False

    def click_button(self, element_key):
        try:
            print(f"Clicking the button {element_key}")
            _element = self.find_element(element_key)
            _element = WebDriverWait(self.browser, self.timeout).until(ec.element_to_be_clickable(_element))
            _element.click()
            print(f"Successfully clicked the button {element_key}")
        except TimeoutException:
            raise AssertionError(f"def:click_button() - {element_key} is not visible within specified time")
        except Exception as e:
            raise AssertionError(f"def:click_button() - Unable to Click the element {element_key} -> {e}")

    def click_by_script(self, element_key):
        try:
            print(f"Clicking the button {element_key}")
            _element = self.find_web_element(element_key)
            self.browser.execute_script("arguments[0].click();", _element)
            print(f"Successfully clicked the button {element_key}")
        except Exception as e:
            raise AssertionError(f"def:click_by_script() - Unable to Click the element {element_key} -> {e}")

    def ews_move_to_element_and_click(self, element_key, offset=(0, 0)):
        try:
            print(f"Clicking the button {element_key}")
            _element = self.find_web_element(element_key)
            if offset == (0, 0):
                self.action.move_to_element(_element).click().perform()
            else:
                self.action.move_to_element_with_offset(_element, offset[0], offset[1]).click().perform()
            print(f"Successfully clicked the button {element_key}")
        except Exception as e:
            raise AssertionError(
                f'def:move_to_element_and_click() - Unable to Click the element {element_key} -> {e}')

    def is_checkbox_checked(self, element_key):
        try:
            print(f'Getting the Checkbox status for - {element_key}')
            return self.find_web_element(element_key).is_selected()
        except Exception as e:
            raise AssertionError(f'def:is_checkbox_checked() - Unable to get the status of Checkbox -> {e}')

    def check_checkbox(self, element_key):
        try:
            print(f'Checking the Checkbox - {element_key}')
            _element = self.find_web_element(element_key)
            if not _element.is_selected():
                _element.click()
            print(f'Successfully Checked the checkbox - {element_key}')
        except Exception as e:
            raise AssertionError(f'def:check_checkbox() - Unable to Check the Checkbox -> {e}')

    def uncheck_checkbox(self, element_key):
        try:
            print(f'Unchecking the Checkbox - {element_key}')
            _element = self.find_web_element(element_key)
            if _element.is_selected():
                _element.click()
            print(f'Successfully Unchecked the checkbox - {element_key}')
        except Exception as e:
            raise AssertionError(f'def:uncheck_checkbox() - Unable to Uncheck the Checkbox -> {e}')

    def ews_get_body_text(self):
        try:
            return self.browser.find_element_by_tag_name('body').text
        except Exception as e:
            raise AssertionError(f'def:ews_get_body_text() - Unable to get body text -> {e}')
        