import re, json
import requests
from datetime import datetime
from log import log
from config import config
from parse_tasks import execute_tasks
from slack_tasks import parse_for_slack
from s3 import load_data_from_bucket


class Parser:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def run(self):
        log.info('Starting Parse')
        data = self.load()
        data = self.parse(data)
        self.post(data)

    def post(self, data):
        if config['slack']['webhook']:
            log.info('Post to slack 🚢 ')
            for d in data:
                for_slack = parse_for_slack(d)
                self.post_to_slack(for_slack)

        elif config['server']['url']:
            log.info('Post to server 🚢 ')


    def post_to_slack(self, text):
        r = requests.post(config['slack']['webhook'],  data=json.dumps({'text': text}))
        if r.status_code == requests.codes.ok:
            log.info("posted to slack".format(text))
        else:
            log.error("Response Body: {}".format(r.text))

    def post_to_server(self):
        pass

    def parse(self, data):
        for d in data:
            d['parsed'] = execute_tasks(d['raw'])
        return data

    def load(self):
        if config['firebase']['apiKey']:
            return self.load_from_firebase()

        elif config['s3']['access_key_id']:
            return self.load_from_s3()

        log.error('s3, firbase config missing ')
        return  {}

    def load_from_s3(self):
        log.info('Loading data from s3')
        data = load_data_from_bucket()
        scrapes = []
        for key, body in data:
            scrape_date = re.search('(\d{4}-\d{2}-\d{2})', key)
            if config['today_only']:
                if scrape_date.group(1) == datetime.now().strftime('%Y-%m-%d'):
                    log.info('Only parsing scrapes from today')
                    scrapes.append({'date': scrape_date.group(1), 'raw': body})
            else:
                scrapes.append({'date': scrape_date.group(1), 'raw': body})

        return scrapes

    def load_from_firebase(self):
        log.info('Loading data from firebase')

