# A set of extensions to the functions normally provided by the selenium
# webdriver. These are primarily for parsing and searching.
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlparse
import random
import time


def scroll_down(driver):
    at_bottom = False
    while random.random() > .20 and not at_bottom:
        k = str(10 + int(200*random.random()))
        driver.execute_script("window.scrollBy(0,"+k+")")
        at_bottom = driver.execute_script("return (((window.scrollY + window.innerHeight ) +100 > document.body.clientHeight ))")
        time.sleep(0.5 + random.random())


def scroll_down_full(driver):
    at_bottom = False
    while not at_bottom:
        # k = str(10 + int(200*random.random()))
        k = str(500)
        driver.execute_script("window.scrollBy(0,"+k+")")
        at_bottom = driver.execute_script("return (((window.scrollY + window.innerHeight ) + 200 > document.body.clientHeight ))")
        time.sleep(0.8)


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    return


def is_loaded(webdriver):
    return (webdriver.execute_script("return document.readyState") == "complete")


def wait_until_loaded(webdriver, timeout, period=0.25):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if is_loaded(webdriver):
            return True
        time.sleep(period)
    return False


def get_intra_links(webdriver, url):
    domain = urlparse(url).hostname
    links = filter(lambda x: (x.get_attribute("href") and x.get_attribute("href").find(domain) > 0 and x.get_attribute("href").find("http") == 0), webdriver.find_elements_by_tag_name("a"))
    return links

# Search/Block Functions
# locator_type: a text representation of the standard
# webdriver.find_element_by_* functions. You can either
# import selenium.webdriver.common.by.By and use By.LINK_TEXT, etc.
# or just remember the string representations. For example:
# By.LINK_TEXT is 'link text'
# By.CSS_SELECTOR is 'css selector'
# By.NAME is 'name' ... and so on
# locator: string that you are looking for


def wait_and_find(driver, locator_type, locator, timeout=3, check_iframes=True):
    if is_found(driver, locator_type, locator, timeout):
        return driver.find_element(locator_type, locator)
    else:
        if check_iframes: # this may return the browser with an iframe active
            driver.switch_to_default_content()
            iframes = driver.find_elements_by_tag_name('iframe')

            for iframe in iframes:
                driver.switch_to_default_content()
                driver.switch_to_frame(iframe)
                if is_found(driver, locator_type, locator, timeout=0):
                    return driver.find_element(locator_type, locator)

            # If we get here, search also fails in iframes
            driver.switch_to_default_content()
        raise NoSuchElementException("Element not found during wait_and_find")


def is_found(driver, locator_type, locator, timeout=3):
    try:
        w = WebDriverWait(driver, timeout)
        w.until(lambda d: d.find_element(locator_type, locator))
        return True
    except TimeoutException:
        return False


def is_visible(driver, locator_type, locator, timeout=3):
    try:
        w = WebDriverWait(driver, timeout)
        w.until(EC.visibility_of_element_located((locator_type, locator)))
        return True
    except TimeoutException:
        return False


def title_is(driver, title, timeout=3):
    try:
        w = WebDriverWait(driver, timeout)
        w.until(EC.title_is(title))
        return True
    except TimeoutException:
        return False


def title_contains(driver, title, timeout=3):
    try:
        w = WebDriverWait(driver, timeout)
        w.until(EC.title_contains(title))
        return True
    except TimeoutException:
        return False