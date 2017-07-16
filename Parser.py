from log import log
from config import config
from s3 import load_data_from_bucket


class Parser:
    def __init__(self):
        self.use_firebase = True if config['firebase']['apiKey'] else False
        self.use_s3 = True if config['s3']['access_key_id'] else False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def run(self):
        if self.use_firebase:
            self.load_from_firebase()

        if self.use_s3:
            self.load_from_s3()

    def load_from_s3(self):
        log.info('Loading data from s3')
        data = load_data_from_bucket()
        for key, body in data:
            print(key)
            print(body)

    def load_from_firebase(self):
        log.info('Loading data from firebase')

    def post_to_slack(self):
        pass

    def post_to_server(self):
        pass
