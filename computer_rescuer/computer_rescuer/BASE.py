import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = os.path.dirname(__file__) + '\\..\\..\\env.ini'
load_dotenv(dotenv_path)

#DB情報
DB_ENGINE=os.environ.get('DB_ENGINE')
DB_NAME=os.environ.get('DB_NAME')
DB_USER=os.environ.get('DB_USER')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
DB_HOST=os.environ.get('DB_HOST')
DB_PORT=os.environ.get('DB_PORT')

TOKEN_LIFETIME=os.environ.get('TOKEN_LIFETIME')
