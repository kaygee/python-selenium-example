from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import MoveTargetOutOfBoundsException
import unittest

TARGET_URL = 'http://www.slapkirk.com/play'
WAIT_SPOCK_HAND = (By.CSS_SELECTOR, 'fa-hand-spock-o')
WAIT_SPOCK_HAND_SPINNER = (By.CSS_SELECTOR, 'fa-spin')
KIRK_IMAGE = (By.ID, 'animationImage')
SCORE_BOX = (By.ID, 'scoreBox')

WAIT = 30
SLAP_COUNT = 1000
OFFSET_INCREMENT = 30
Y_OFFSET = 100
BROWSER_WINDOW_HEIGHT = 600
BROWSER_WINDOW_WIDTH = 875


class SlapKirkTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(BROWSER_WINDOW_WIDTH, BROWSER_WINDOW_HEIGHT)
        self.driver.get(TARGET_URL)
        self.wait_for_loading()

    def tearDown(self):
        self.driver.quit()

    def test_slap_kirk(self):
        for num in range(0, SLAP_COUNT):
            self.slap_kirk_left()
            self.slap_kirk_right()
        self.print_score()

    def print_score(self):
        score = self.wait_for_something(EC.visibility_of_element_located(SCORE_BOX))
        print(score.text)

    def slap_kirk_left(self):
        kirk_image = self.wait_for_kirk_image()
        left_side_of_image = 0 + OFFSET_INCREMENT
        self.move_to_offset_of_element(kirk_image, left_side_of_image)

    def slap_kirk_right(self):
        kirk_image = self.wait_for_kirk_image()
        right_side_of_image = kirk_image.size['width'] - OFFSET_INCREMENT
        self.move_to_offset_of_element(kirk_image, right_side_of_image)

    def move_to_offset_of_element(self, to_element, x_offset):
        try:
            ActionChains(self.driver).move_to_element_with_offset(to_element, x_offset, Y_OFFSET).perform()
        except MoveTargetOutOfBoundsException:
            print("Tried to move to offset but couldn't!")

    def wait_for_loading(self):
        self.wait_for_something(EC.invisibility_of_element_located(WAIT_SPOCK_HAND))
        self.wait_for_something(EC.invisibility_of_element_located(WAIT_SPOCK_HAND_SPINNER))
        self.wait_for_something(EC.presence_of_element_located(KIRK_IMAGE))

    def wait_for_kirk_image(self):
        kirk_image = self.wait_for_something(EC.presence_of_element_located(KIRK_IMAGE))
        return kirk_image

    def wait_for_something(self, expected_condition):
        return WebDriverWait(self.driver, WAIT).until(expected_condition)

if __name__ == '__main__':
    unittest.main()
