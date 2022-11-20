from typing import Dict

from main.models.constraints import Constraints


class ExplanationRequirement:
    def __init__(self, json: Dict[str, any]):
        self.id = json["_id"]
        self.original_image = json.get("original_image", "")
        self.original_image_id = json.get("original_image_id")
        self.constraints = Constraints(json)

    def to_db_value(self) -> Dict[str, any]:
        return {
            '_id': self.id,
            'original_image': self.original_image,
            'original_image_id': self.original_image_id,
            'constraints': self.constraints.to_db_value(),
        }