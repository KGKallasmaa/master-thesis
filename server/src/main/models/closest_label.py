from typing import Dict

from bson import ObjectId


class ClosestLabel:
    def __init__(self, json: Dict[str, any]):
        self.id = json.get("_id",str(ObjectId()))
        self.image_index = json.get("image_index", "")
        self.label = json.get("label", "")
        self.closest = json.get("closest", [])

    def to_db_value(self) -> Dict[str, any]:
        return {
            '_id': self.id,
            'image_index': self.image_index,
            'label': self.label,
            'closest': self.closest,
        }
