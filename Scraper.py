import os, json, time, random, pickle, firefoxUtils.deploy_firefox, signal
from selenium.webdriver import ActionChains
from webdriver_extensions import scroll_down
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Firebase import Firebase
from log import log
from s3 import upload_strings
from config import config
from os.path import abspath, join, dirname
from scrape_tasks import execute_tasks
from datetime import datetime

SELECTORS = {}
DEFAULT_SLEEP = 3
NUM_MOUSE_MOVES = 2
RANDOM_SLEEP_LOW = 1
RANDOM_SLEEP_HIGH = 7


class Scraper:
    def __init__(self):
        self.user = config['scrape_info']['user']
        self.passwd = config['scrape_info']['pass']
        self.scraped = {}
        if config['scrape_info']['local']:
            log.info('Saving data locally.')
        self.save_local = config['scrape_info']['local']
        self.display_pid = None
        self.display_port = None
        self.firebase = Firebase()
        self.timestamp = ''
        self.webdriver = self._init_browser()

    def _init_browser(self):
        driver, browser_profile_path, profile_settings = \
            firefoxUtils.deploy_firefox.deploy_firefox(config['browser_params'])
        return driver

    def add_cookies(self):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.webdriver.add_cookie(cookie)

    def run(self):
        try:
            self.timestamp = datetime.now().strftime("%Y-%m-%d")
            self.get_website(config['scrape_info']['url'])
            if config['browser_params']['save_cookies']:
                self.add_cookies()

            result = execute_tasks(self.webdriver, self.user, self.passwd)
            self.save_html()
            # if not self.save_local:
            #     self.firebase.upload(self.scraped)
        except Exception as e:
            log.error("Scrape error")
            log.error(e)

    def get_website(self, url=None):
        log.info('get_website %s' % url)
        main_handle = self.webdriver.current_window_handle
        try:
            if url:
                self.webdriver.get(url)
            else:
                self.webdriver.get(self.url)

        except TimeoutException:
            log.error('[get_website] TimeoutException')

        # Sleep after get returns
        time.sleep(DEFAULT_SLEEP)

        # Close modal dialog if exists
        try:
            WebDriverWait(self.webdriver, .5).until(EC.alert_is_present())
            alert = self.webdriver.switch_to_alert()
            alert.dismiss()
            time.sleep(1)
        except TimeoutException:
            pass

        windows = self.webdriver.window_handles
        if len(windows) > 1:
            for window in windows:
                if window != main_handle:
                    self.webdriver.switch_to_window(window)
                    self.webdriver.close()
            self.webdriver.switch_to_window(main_handle)

        if config['browser_params']['bot_mitigation']:
            self.bot_mitigation()

    def bot_mitigation(self):
        """Three commands for bot-detection mitigation when getting a site."""
        # bot mitigation 1: move the randomly around a number of times
        window_size = self.webdriver.get_window_size()
        num_moves = 0
        num_fails = 0
        while num_moves < NUM_MOUSE_MOVES + 1 and num_fails < NUM_MOUSE_MOVES:
            try:
                if num_moves == 0:  # move to the center of the screen
                    x = int(round(window_size['height']/2))
                    y = int(round(window_size['width']/2))
                else:  # move a random amount in some direction
                    move_max = random.randint(0, 500)
                    x = random.randint(-move_max, move_max)
                    y = random.randint(-move_max, move_max)
                action = ActionChains(self.webdriver)
                action.move_by_offset(x, y)
                action.perform()
                num_moves += 1

            except MoveTargetOutOfBoundsException:
                num_fails += 1
                self.log.warning("Mouse movement out of bounds,"
                                 "trying a different offset...")

        # bot mitigation 2: scroll in random intervals down page
        scroll_down(self.webdriver)

        # mitigation 3: randomly wait so that page visits appear irregularly
        time.sleep(random.randrange(RANDOM_SLEEP_LOW, RANDOM_SLEEP_HIGH))

    def save_html(self):
        filename = "%s-%s-%s.html" % (config['scrape_info']['name'], self.timestamp, self.user) if self.user else "%s-%s.html" % (config['scrape_info']['name'], self.timestamp)
        src = self.webdriver.execute_script('return document.documentElement.innerHTML')

        if self.save_local:
            with open(os.path.join(config['output-folder'], filename), 'w') as outfile:
                outfile.write(src)
        else:
            upload_strings(src, filename)

    def save_json(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.webdriver:
            pickle.dump(self.webdriver.get_cookies(), open("cookies.pkl", "wb"))
            self.webdriver.quit()

        if self.display_pid is not None:
            try:
                os.kill(self.display_pid, signal.SIGKILL)
            except OSError:
                log.debug("Headless(Display) process does not exit")
                pass
            except TypeError:
                log.error(" PID may not be the correct type %s" %
                          (str(self.display_pid)))

        if self.display_port is not None:  # xvfb diplay lock
            try:
                os.remove("/tmp/.X" + str(self.display_port) + "-lock")
            except OSError:
                log.debug("Screen lockfile already removed")
                pass

        os.system("killall -9 firefox")
        os.system("killall -9 Xvfb")
