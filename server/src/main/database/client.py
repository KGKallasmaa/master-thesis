import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()


def get_client() -> MongoClient:
    url = os.getenv("DB_URL")
    return MongoClient(url, server_api=ServerApi('1'))