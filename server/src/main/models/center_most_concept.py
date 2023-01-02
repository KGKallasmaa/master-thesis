from typing import Dict


class CenterMostConcept:
    def __init__(self, json: Dict[str, any]):
        self.concept_name = json["conceptName"]
        self.src = json["src"]
        self.distance = json["distance"]

    def to_db_value(self) -> Dict[str, any]:
        return {
            'conceptName': self.concept_name,
            'src': self.src,
            'distance': self.distance,
        }
