from typing import List, Optional

from main.database.client import get_client
from main.models.consept_intuitevness import ConceptIntuitiveness


class IntuitivenessDb:
    def __init__(self, client=get_client()):
        self.database = client.get_database("most_intuitive_concepts")
        self.collection = self.database["most_intuitive_concepts"]

    def get_constraint_by_concept(self, concept: str) -> Optional[ConceptIntuitiveness]:
        value = self.collection.find_one({"concept": concept})
        return None if value is None else ConceptIntuitiveness(value)

    def update_intuitiveness(self, obj: ConceptIntuitiveness):
        try:
            result = self.collection.update_one({'label': obj.label}, {'$set': obj.to_db_value()}, upsert=True)
            return result.matched_count > 0
        except Exception:
            return False

    def top_intuitive_concepts(self, label: str, limit: int) -> List[ConceptIntuitiveness]:
        query = self.collection.find({"label": label}).sort("count", -1).limit(limit)
        return [ConceptIntuitiveness(el) for el in query]
