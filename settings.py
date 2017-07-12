import os, __main__
from os.path import join, dirname, abspath
from config import config
import dotenv

dotenv_path = abspath(join(dirname(__file__), '.env'))
dotenv.load_dotenv(dotenv_path)

USER = os.environ.get('USERNAME') if os.environ.get('USERNAME') else False
PASS = os.environ.get('PASS') if os.environ.get('PASS') else False