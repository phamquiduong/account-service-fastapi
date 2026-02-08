import os
from datetime import timedelta

from constants.server import Environment

ENVIRONMENT: Environment = Environment(os.getenv("ENVIRONMENT", "development").lower())

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(minutes=5)
REFRESH_TOKEN_EXPIRE = timedelta(days=60)
