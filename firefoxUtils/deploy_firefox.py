import firefoxUtils.configure_firefox
import logging
import logging
import shutil
import os
import random
import platform
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from pyvirtualdisplay import Display

logger = logging.getLogger(__name__)

DEFAULT_SCREEN_RES = (1366, 768)  # Default screen res when no preferences are given

def deploy_firefox( browser_params):
    """ launches a firefox instance with parameters set by the input dictionary """
    root_dir = os.path.dirname(__file__)  # directory of this file
    display_pid = None
    display_port = None
    fp = webdriver.FirefoxProfile()
    browser_profile_path = fp.path + '/'

    profile_settings = None  # Imported browser settings

    # If profile settings still not set - set defaults
    if profile_settings is None:
        profile_settings = dict()
        profile_settings['screen_res'] = DEFAULT_SCREEN_RES #browser_params['screen_res']
        profile_settings['ua_string'] = browser_params['ua_string']

    if profile_settings['ua_string'] is not None:
        logger.info("Setting UA:{}... ".format((browser_params['ua_string'][:50])))
        fp.set_preference("general.useragent.override", profile_settings['ua_string'])

    if browser_params['headless']:
        display = Display(visible=0, size=profile_settings['screen_res'])
        display.start()
        display_pid = display.pid
        display_port = display.cmd_param[5][1:]
    # status_queue.put(('STATUS','Display',(display_pid, display_port)))
        # logger.debug("Display pid:{} , port: {} ".format((display_pid,display_port)))

    # if browser_params['debugging']:
    #     firebug_loc = os.path.join(root_dir, 'firefox_extensions/firebug-1.11.0.xpi')
    #     fp.add_extension(extension=firebug_loc)
    #     fp.set_preference("extensions.firebug.currentVersion", "1.11.0")  # Avoid startup screen

    # if browser_params['extension']['enabled']:
    #     ext_loc = os.path.join(root_dir + "/../", 'Extension/firefox/@openwpm-0.0.1.xpi')
    #     ext_loc = os.path.normpath(ext_loc)
    #     fp.add_extension(extension=ext_loc)
    #     with open(browser_profile_path + 'database_settings.txt', 'w') as f:
    #         host, port = manager_params['aggregator_address']
    #         crawl_id = browser_params['crawl_id']
    #         f.write(host + ',' + str(port) + ',' + str(crawl_id))
    #         f.write(','+str(browser_params['extension']['cookieInstrument']))
    #         f.write(','+str(browser_params['extension']['jsInstrument']))
    #         f.write(','+str(browser_params['extension']['cpInstrument']))
    #     logger.debug("BROWSER %i: OpenWPM Firefox extension loaded" % browser_params['crawl_id'])


    # Disable flash
    if browser_params['disable_flash']:
        fp.set_preference('plugin.state.flash', 0)

    # Configure privacy settings
    firefoxUtils.configure_firefox.privacy(browser_params, fp, "", "")

    # Set various prefs to improve speed and eliminate traffic to Mozilla
    firefoxUtils.configure_firefox.optimize_prefs(fp)

    # Launch the webdriver
    # if platform.system() == "Darwin":
    #     fb = FirefoxBinary("/Applications/Firefox.app/Contents/MacOS/firefox")
    # else:
    #     fb = FirefoxBinary(root_dir  + "/../../firefox-bin/firefox")
    # # fb = FirefoxBinary("/Users/surya/Code/OpenWPM/Firefox.app/Contents/MacOS/firefox")
    # driver = webdriver.Firefox(firefox_profile=fp, firefox_binary=fb)

    driver = webdriver.Firefox(firefox_profile=fp)
    # print(dir(driver.binary))
    # logger.info('Browser Launched pid: {}  '.format(int(driver.binary.process.pid)))

    # set window size
    driver.set_window_size(*profile_settings['screen_res'])

    return driver, browser_profile_path, profile_settings
