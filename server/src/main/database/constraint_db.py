
from main.database.client import get_client
from main.models.constraints import Constraints


class ConstraintDb:
    def __init__(self, client=get_client()):
        self.database = client.get_database("constraint")
        self.collection = self.database["constraint"]

    def get_constraint_by_explanation_requirement_id(self, id: str) -> Constraints:
        value = self.collection.find_one({"explanation_requirement_id": id})
        if value is None:
            return Constraints({"explanation_requirement_id": id})
        return Constraints(value)

    def update_constraint(self, obj: Constraints) -> bool:
        explanation_filter = {'explanation_requirement_id': obj.explanation_requirement_id}
        try:
            result = self.collection.update_one(explanation_filter, {'$set': obj.to_db_value()}, upsert=True)
            return result.matched_count > 0
        except Exception:
            return False
