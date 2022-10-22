from typing import List

from main.database.client import get_client
from main.models.closest_label import ClosestLabel


class ClosestLabelsDb:
    def __init__(self, client=get_client()):
        self.database = client.get_database("closest_labels")
        self.collection = self.database["closest_labels"]

    def get_closest_labels(self, label: str) -> List[str]:
        value = self.collection.find_one({'label': label})
        if value is None:
            return []
        return ClosestLabel(value).closest

    def update_closest_labels(self, obj: ClosestLabel):
        self.collection.update_one({'_id': obj.id}, {'$set': obj.to_db_value()}, upsert=True)
