from typing import Dict

from bson import ObjectId


class ConceptSuggestions:
    def __init__(self, json: Dict[str, any]):
        self.used_concepts = json.get("usedConcepts", [])
        self.available_to_be_chosen_concepts = json.get("availableToBeChosenConcepts", "")

    def to_db_value(self) -> Dict[str, any]:
        return {
            'usedConcepts"': self.used_concepts,
            'availableToBeChosenConcepts': self.available_to_be_chosen_concepts,
        }
