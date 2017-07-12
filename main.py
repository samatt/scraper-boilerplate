from Scraper import Scraper
from config import config


with Scraper(user=config['scrape_info']['user'],
             passwd=config['scrape_info']['pass'],
             save_local=config['scrape_info']['local']) as scraper:
    scraper.run()
