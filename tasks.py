from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
from log import log
from datetime import datetime, timedelta


def execute_tasks(webdriver, user=None, passwd=None):
    try:
        if user:
            click_login(webdriver)
            nav_sign_in(webdriver, user, passwd)
        faraa_document_search(webdriver)
        return True
    except Exception as e:
        log.error("⚠️  Scrape error: %s" % e)
        return False


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


def faraa_document_search(webdriver):
    num_days = 7
    frame = webdriver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[2]/p[2]/iframe')
    webdriver.switch_to.frame(frame)
    select = Select(webdriver.find_element_by_id('P10_DOCTYPE'))
    select.select_by_visible_text('ALL')
    webdriver.find_element(By.CSS_SELECTOR, 'input[id^="P10_STAMP1"]').send_keys((datetime.now() - timedelta(days=num_days)).strftime('%m/%d/%Y'))
    webdriver.find_element(By.CSS_SELECTOR, 'input[id^="P10_STAMP2"]').send_keys(datetime.now().strftime('%m/%d/%Y'))
    webdriver.find_element_by_id('SEARCH').click()
    time.sleep(5)
