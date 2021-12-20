from typing import Dict


class ExplanationRequirement:
    def __init__(self, id: str):
        self.id = id
        self.available_concepts = []

    def set_available_concepts(self, available_concepts: list):
        self.available_concepts = available_concepts

    def to_db_value(self) -> Dict[str, any]:
        return {
            'id': self.id,
            'available_concepts': self.available_concepts,
        }