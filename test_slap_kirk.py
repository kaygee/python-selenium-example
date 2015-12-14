import datetime
from peewee import *
from selenium import webdriver
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

db = SqliteDatabase('slap_kirk.db')

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
DRIVER = webdriver.Chrome()


class SlapKirk(Model):
    slap_count = IntegerField()
    offset_increment = IntegerField()
    browser_width = IntegerField()
    slaps_per_second = DecimalField()
    browser_driver = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def setup_webdriver():
    DRIVER.set_window_size(BROWSER_WINDOW_WIDTH, BROWSER_WINDOW_HEIGHT)
    DRIVER.get(TARGET_URL)


def teardown_webdriver():
    DRIVER.quit()


def slap_captain_kirk():
    wait_for_load()
    for num in range(0, SLAP_COUNT):
        slap_kirk_left()
        slap_kirk_right()


def print_score():
    score_element = wait_for_something(EC.visibility_of_element_located(SCORE_BOX))
    score = score_element.text
    split_score = score.split()
    print("Slap count {} running at {} slaps per second.".format(split_score[2], split_score[4]))
    return split_score


def initialize():
    # Create the database and the table if they don't exist
    db.connect()
    db.create_tables([SlapKirk], safe=True)


def slap_kirk_left():
    kirk_image = wait_for_kirk_image()
    left_side_of_image = 0 + OFFSET_INCREMENT
    move_to_offset_of_element(kirk_image, left_side_of_image)


def slap_kirk_right():
    kirk_image = wait_for_kirk_image()
    right_side_of_image = kirk_image.size['width'] - OFFSET_INCREMENT
    move_to_offset_of_element(kirk_image, right_side_of_image)


def move_to_offset_of_element(to_element, x_offset):
    try:
        ActionChains(DRIVER).move_to_element_with_offset(to_element, x_offset, Y_OFFSET).perform()
    except MoveTargetOutOfBoundsException:
        print("Tried to move to offset but couldn't!")


def wait_for_load():
    wait_for_something(EC.invisibility_of_element_located(WAIT_SPOCK_HAND))
    wait_for_something(EC.invisibility_of_element_located(WAIT_SPOCK_HAND_SPINNER))
    wait_for_something(EC.presence_of_element_located(KIRK_IMAGE))


def wait_for_kirk_image():
    kirk_image = wait_for_something(EC.presence_of_element_located(KIRK_IMAGE))
    return kirk_image


def wait_for_something(expected_condition):
    return WebDriverWait(DRIVER, WAIT).until(expected_condition)


def add_score():
    SlapKirk.create(
            slap_count=SLAP_COUNT,
            offset_increment=OFFSET_INCREMENT,
            browser_width=BROWSER_WINDOW_WIDTH,
            slaps_per_second=split_score[4],
            browser_driver=DRIVER.name
    )


def print_scores():
    entries = SlapKirk.select().order_by(SlapKirk.timestamp.desc())
    print("Previous results slapping Captain Kirk!")
    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print('=' * len(timestamp))
        print("Slap count {}".format(entry.slap_count))
        print("Browser {}".format(entry.browser_driver))
        print("Width offset {}".format(entry.offset_increment))
        print("Slaps per second {}".format(entry.slaps_per_second))
        print("\n")


if __name__ == '__main__':
    db.connect()
    db.create_tables([SlapKirk], safe=True)
    print_scores()
    setup_webdriver()
    slap_captain_kirk()
    split_score = print_score()
    teardown_webdriver()
    add_score()

