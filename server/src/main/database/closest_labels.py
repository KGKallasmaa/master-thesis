from typing import Optional

from main.database.client import get_client
from main.models.closest_label import ClosestLabel


class ClosestLabelsDb:
    def __init__(self, client=get_client()):
        self.database = client.get_database("closest_labels")
        self.collection = self.database["closest_labels"]

    def get_by_image_id(self, image_id: int) -> Optional[ClosestLabel]:
        value = self.collection.find_one({'image_index': image_id})
        return None if value is None else ClosestLabel(value)

    def update_closest_labels(self, obj: ClosestLabel):
        self.collection.update_one({'_id': obj.id}, {'$set': obj.to_db_value()}, upsert=True)
