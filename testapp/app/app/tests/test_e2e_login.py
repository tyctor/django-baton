import time

from django.test import TestCase
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()


class TestBatonLogin(TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=chrome_options,)

    def test_form(self):
        self.driver.get('http://localhost:8000/admin')
        # wait for page to load
        try:
            element_present = EC.presence_of_element_located(
                (By.ID, 'header'))
            WebDriverWait(self.driver, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        time.sleep(1)
        header_field = self.driver.find_element_by_id("header")
        print(header_field.text)
        self.assertEqual(header_field.text, 'Baton Test App')

        username_field = self.driver.find_element_by_id("id_username")
        password_field = self.driver.find_element_by_id("id_password")
        button = self.driver.find_element_by_css_selector('input[type=submit]')
        self.assertEqual(password_field.is_displayed(), True)
        self.assertEqual(username_field.is_displayed(), True)
        self.assertEqual(button.is_displayed(), True)

        username_field.send_keys('admin')
        time.sleep(1)
        password_field.send_keys('admin')
        time.sleep(1)
        button.click()
        self.assertEqual(self.driver.current_url, 'http://localhost:8000/admin/')
