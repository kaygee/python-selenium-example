import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import string
import unittest

TARGET_URL = 'https://target.url.com'
USERNAME = 'username'
PASSWORD = 'password'

SIGN_IN_BUTTON = '#signInButton'
USERNAME_FIELD = '#username'
PASSWORD_FIELD = '#password'
DISABLED_MSG = '.disabled-explanation'
SESSION_CHECK_MSG = '#lifetechSessionCheckMsg'
DESIGN_NAME_FIELD = '#designName'
MORE_BUTTON = '#expandNewDesignFormDiv'
NEXT_ADD_TARGETS_BUTTON = '#saveDesign'
GENE_CDS_ONLY_RADIO = "[value='GENE_CDS']"
TARGET_NAME = '#targetRegion_new_name'
ADD_TARGET_BUTTON = '#targetRegion_new_saveTarget'
REGION_RADIO = "[value='REGION']"

WAIT = 30


class SeleniumIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test_add_target_to_design(self):
        self.driver.get(TARGET_URL)
        assert "Ion AmpliSeq™ Designer" in self.driver.title

        import pdb; pdb.set_trace()

        sign_in_button = self.driver.find_element_by_css_selector(SIGN_IN_BUTTON)
        sign_in_button.click()

        self.set_username_field(USERNAME)

        password_field = self.driver.find_element_by_css_selector(PASSWORD_FIELD)
        password_field.send_keys(PASSWORD)

        # http://docs.seleniumhq.org/exceptions/stale_element_reference.jsp
        sign_in_button = self.driver.find_element_by_css_selector(SIGN_IN_BUTTON)
        sign_in_button.click()

        random_design_name = self.random_string_generator()
        self.set_design_name_field(random_design_name)

        self.click_next_add_targets()

        self.add_gene_cds_only_target("BRCA1")

    def add_gene_cds_only_target(self, target_name):
        self.wait_and_click((By.CSS_SELECTOR, GENE_CDS_ONLY_RADIO))
        self.wait_for_visibility_and_send_keys((By.CSS_SELECTOR, TARGET_NAME), target_name)
        self.click_add_target_button()

    def click_add_target_button(self):
        self.wait_and_click((By.CSS_SELECTOR, ADD_TARGET_BUTTON))
        self.wait_for_clickable((By.CSS_SELECTOR, ADD_TARGET_BUTTON))
        self.wait_for_all_elements((By.CSS_SELECTOR, "#targetsTable .target-edit"))

    def set_username_field(self, username):
        WebDriverWait(self.driver, WAIT).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, DISABLED_MSG)))
        WebDriverWait(self.driver, WAIT).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, SESSION_CHECK_MSG)))
        WebDriverWait(self.driver, WAIT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, SIGN_IN_BUTTON)))
        username_field_locator = (By.CSS_SELECTOR, USERNAME_FIELD)
        self.wait_for_visibility_and_send_keys(username_field_locator, username)

    def set_design_name_field(self, design_name):
        design_name_locator = (By.CSS_SELECTOR, DESIGN_NAME_FIELD)
        self.wait_for_visibility_and_send_keys(design_name_locator, design_name)
        WebDriverWait(self.driver, WAIT).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, MORE_BUTTON)))

    def click_next_add_targets(self):
        self.wait_and_click((By.CSS_SELECTOR, NEXT_ADD_TARGETS_BUTTON))

    def wait_for_visibility_and_send_keys(self, locator, text):
        element_to_send_keys = WebDriverWait(self.driver, WAIT).until(EC.visibility_of_element_located(locator))
        element_to_send_keys.send_keys(text)

    def wait_for_all_elements(self, locator):
        WebDriverWait(self.driver, WAIT).until(EC.presence_of_all_elements_located(locator))

    def wait_for_clickable(self, locator):
        WebDriverWait(self.driver, WAIT).until(EC.element_to_be_clickable(locator))

    def wait_and_click(self, locator):
        element_to_click = WebDriverWait(self.driver, WAIT).until(EC.element_to_be_clickable(locator))
        element_to_click.click()

    def random_string_generator(self, size=25, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    unittest.main()
