from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import MoveTargetOutOfBoundsException
import unittest

TARGET_URL = 'http://www.slapkirk.com/play'
WAIT_SPOCK_HAND = 'fa-hand-spock-o'
WAIT_SPOCK_HAND_SPINNER = 'fa-spin'
ANIMATION_IMAGE = '#animationImage'
ANIMATION_FRAME = '#animationFrame'
ANIMATION_ALERT_FRAME = '#animationAlertFrame'
SCORE_BOX = '#scoreBox'
Y_OFFSET = 100

WAIT = 30


class SlapKirkTest(unittest.TestCase):

    def setUp(self):
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        self.driver.get(TARGET_URL)
        self.wait_for_something(EC.invisibility_of_element_located((By.CSS_SELECTOR, WAIT_SPOCK_HAND)))
        self.wait_for_something(EC.invisibility_of_element_located((By.CSS_SELECTOR, WAIT_SPOCK_HAND_SPINNER)))
        self.wait_for_something(EC.presence_of_element_located((By.CSS_SELECTOR, ANIMATION_IMAGE)))

    def tearDown(self):
        self.driver.quit()

    def test_slap_kirk(self):
        for num in range(0, 1000):
            self.move_left()
            self.move_right()
        self.print_score()

    def print_score(self):
        score = self.wait_for_something(EC.visibility_of_element_located((By.CSS_SELECTOR, SCORE_BOX)))
        # Slap Count: 39 SPS: 0.0
        print(score.text)

    def move_left(self):
        kirk_image = self.wait_for_kirk_image()
        left_side_of_image = 0 + 10
        self.move_to_offset_of_element(kirk_image, left_side_of_image)

    def move_right(self):
        kirk_image = self.wait_for_kirk_image()
        right_side_of_image = kirk_image.size['width'] - 10
        self.move_to_offset_of_element(kirk_image, right_side_of_image)

    def move_to_offset_of_element(self, to_element, x_offset):
        try:
            ActionChains(self.driver).move_to_element_with_offset(to_element, x_offset, Y_OFFSET).perform()
        except MoveTargetOutOfBoundsException:
            print("Tried to move to offset but couldn't!")

    def wait_for_kirk_image(self):
        self.wait_for_something(EC.presence_of_element_located((By.CSS_SELECTOR, ANIMATION_IMAGE)))
        kirk_image = self.driver.find_element_by_css_selector(ANIMATION_IMAGE)
        return kirk_image

    def wait_for_something(self, expected_condition):
        return WebDriverWait(self.driver, WAIT).until(expected_condition)

if __name__ == '__main__':
    unittest.main()
