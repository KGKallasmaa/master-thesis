from typing import Dict


class ExplanationRequirement:
    def __init__(self, json: Dict[str, any]):
        self.id = json["_id"]
        self.available_concepts = json.get("available_concepts", [])
        self.original_image = json.get("original_image", "")
        self.original_image_id = json.get("original_image_id")

    def to_db_value(self) -> Dict[str, any]:
        return {
            '_id': self.id,
            'available_concepts': self.available_concepts,
            'original_image': self.original_image,
            'original_image_id': self.original_image_id
        }
