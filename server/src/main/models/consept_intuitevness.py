from typing import Dict

from bson import ObjectId


class ConceptIntuitiveness:
    def __init__(self, json: Dict[str, any]):
        self.id = json.get("_id", str(ObjectId()))
        # e.g. "bedroom"
        self.label = json.get("label", "")
        # e.g. bed
        self.concept = json.get("concept", "")
        self.count = json.get("count",0)

    def to_db_value(self) -> Dict[str, any]:
        return {
            '_id': self.id,
            'label': self.label,
            'concept': self.concept,
            'count': self.count,
        }

    def increment_count(self):
        self.count += 1

    def decrement_count(self):
        self.count -= 1
