from typing import Dict


class CenterMostConcept:
    def __init__(self, json: Dict[str, any]):
        self.concept_name = json["conceptName"]
        self.src = json["src"]
        self.distance = json["distance"]

    def __hash__(self):
        return hash(self.unique_key())

    def __eq__(self, other):
        if isinstance(other, CenterMostConcept):
            return self.to_db_value().__eq__(other.to_db_value())
        return NotImplemented

    def to_db_value(self) -> Dict[str, any]:
        return {
            'conceptName': self.concept_name,
            'src': self.src,
            'distance': self.distance,
        }

    def unique_key(self):
        return self.concept_name + self.src + str(self.distance)
