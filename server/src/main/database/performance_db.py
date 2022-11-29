
from main.database.client import get_client
from main.models.performace import Performance


class PerformanceDb:
    def __init__(self, client=get_client()):
        self.database = client.get_database("performance")
        self.collection = self.database["performance"]

    def get_by_explanation_requirement_id(self, exp_id: str) -> Performance:
        value = self.collection.find_one({"explanationRequirementId": exp_id})
        if value is None:
            return Performance({"explanationRequirementId": exp_id})
        return Performance(value)

    def update(self, obj: Performance) -> bool:
        explanation_filter = {'explanationRequirementId': obj.explanation_requirement_id}
        try:
            result = self.collection.update_one(explanation_filter, {'$set': obj.to_db_value()}, upsert=True)
            return result.matched_count > 0
        except Exception:
            return False
