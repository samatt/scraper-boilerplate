from Scraper import Scraper
from Parser import Parser
from config import config


# with Scraper() as scraper:
#     scraper.run()

with Parser() as parser:
    parser.run()
