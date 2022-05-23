import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

ca = certifi.where()

def get_client() -> MongoClient:
    """Returns the MongoDB client"""
    url = os.getenv("DB_URL")
    return MongoClient(url, server_api=ServerApi('1'), tlsCAFile=ca)
