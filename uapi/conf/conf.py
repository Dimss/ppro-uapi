import os
import logging
from configparser import ConfigParser

# Load configs file
config = ConfigParser(os.environ)
app_ini_file = 'dev.app.ini'
PROFILE = os.environ.get('PROFILE')
if PROFILE and os.environ['PROFILE'] == 'prod':
    app_ini_file = 'prod.app.ini'
logging.info(f"Loading {app_ini_file}")
config.read("{current_dir}/{ini_file}".format(current_dir=os.path.dirname(__file__), ini_file=app_ini_file))

DB_HOST = config.get('db', 'host')
DB_PORT = config.getint('db', 'port')
DB_NAME = config.get('db', 'name')
