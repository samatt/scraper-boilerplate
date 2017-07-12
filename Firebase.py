import pyrebase
from log import log
from config import config


class Firebase:
    def __init__(self):
        if config['firebase']['apiKey']:
            self.fb = pyrebase.initialize_app(config['firebase'])
            self.auth = self.fb.auth()
            self.user = self.auth.sign_in_with_email_and_password(config['firebase']['userId'], config['firebase']['userPassword'])
            self.db = self.fb.database()
        return None

    def upload(self, data):
        result = self.db.child("scrapes").child(data["timestamp"]).set(data, self.user['idToken'])
        log.info(result)
