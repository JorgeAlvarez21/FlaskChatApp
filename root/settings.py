import os
import dotenv

dotenv_file = dotenv.find_dotenv()

dotenv.load_dotenv(dotenv_file)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True


DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'backend/db_instance/db.sqlite')

DEBUG = True if os.getenv('DEBUG').lower() == 'true' else False

CLIENT_HOST = os.getenv('CLIENT_HOST')
CLIENT_PORT = os.getenv('CLIENT_PORT')

SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_PORT = os.getenv('SERVER_PORT')

TMPDIR="backend/db_instance/data/local/tmp"


