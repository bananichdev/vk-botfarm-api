import os

from dotenv import load_dotenv

NAME = "botfarm"
HOST = "0.0.0.0"
PORT = 8000

load_dotenv()

DB_DRIVER = "postgresql"
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_URL = os.environ.get("DB_URL")
DB_NAME = os.environ.get("DB_NAME")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")
ENV = os.environ.get("ENV")

ALGORITHM = os.environ.get("ALGORITHM")
HASH_ROUNDS = os.environ.get("HASH_ROUNDS")
SECRET_KEY = os.environ.get("SECRET_KEY")
DEFAULT_COOKIE_SETTINGS = {"httponly": True}

CLIENT_URL = os.environ.get("CLIENT_URL")
ALLOW_ORIGIN = "http://localhost" if ENV == "stage" else CLIENT_URL

DB_FULL_URL = f"{DB_DRIVER}+asyncpg://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_NAME}"
TEST_DB_FULL_URL = f"{DB_DRIVER}+asyncpg://{DB_USER}:{DB_PASS}@{DB_URL}/{TEST_DB_NAME}"
