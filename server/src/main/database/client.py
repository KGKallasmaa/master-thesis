import os

from pymongo import MongoClient


def get_client() -> MongoClient:
    """Returns the MongoDB client"""
    url = os.getenv("DB_URL")
    try:
        client = MongoClient(url)
    except:
        raise ConnectionError("Could not connect to MongoDB")
    return client
