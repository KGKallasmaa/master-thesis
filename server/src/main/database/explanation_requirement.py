from pymongo import MongoClient

from main.models.explanation_requirement import ExplanationRequirement


class ExplanationRequirementDb:
    def __init__(self, client: MongoClient):
        self.database = client.get_database("explanation_requirement")
        self.collection = self.database["explanation_requirement"]

    def get_explanation_requirement(self, id: str) -> ExplanationRequirement:
        value = self.collection.find_one({'id': id})
        if value is None:
            value = ExplanationRequirement(id)
        return value

    def update_explanation_requirement(self, obj: ExplanationRequirement):
        self.collection.update_one({'id': obj.id}, {'$set': obj.to_db_value()}, upsert=True)
