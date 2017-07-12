from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from log import log


def execute_tasks(webdriver, user=None, passwd=None):
    if user:
        click_login(webdriver)
        nav_sign_in(webdriver, user, passwd)


def click_login(webdriver):
    webdriver.find_element(By.CSS_SELECTOR, 'a[href^="javascript:;"]').click()


def nav_sign_in(webdriver, user, passwd):

    attr = 'name'
    username_value = 'username'
    password_value = 'password'
    username_selector = 'input[%s^="%s"]' % (attr, username_value)
    password_selector = 'input[%s^="%s"]' % (attr, password_value)
    # submit_selector = 'button[type^="submit"]'
    submit_selector = 'button'

    if webdriver.find_elements(By.CSS_SELECTOR, username_selector):
        webdriver.find_element(By.CSS_SELECTOR, username_selector).\
            send_keys(str(user))

        webdriver.find_element(By.CSS_SELECTOR, password_selector).\
            send_keys(str(passwd))

        webdriver.find_element(By.CSS_SELECTOR, submit_selector).click()
        log.info("Signed in with %s" % user)
        time.sleep(30)
    else:
        log.debug('no user form')
