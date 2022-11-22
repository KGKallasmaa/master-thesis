from main.database.client import get_client
from main.models.explanation_requirement import ExplanationRequirement


class ExplanationRequirementDb:
    def __init__(self, client=get_client()):
        self.database = client.get_database("explanation_requirement")
        self.collection = self.database["explanation_requirement"]

    def get_explanation_requirement(self, id: str) -> ExplanationRequirement:
        value = self.collection.find_one({"_id": id})
        if value is None:
            return ExplanationRequirement({"_id": id})
        print(value, flush=True)
        return ExplanationRequirement(value)

    def update_explanation_requirement(self, obj: ExplanationRequirement):
        self.collection.update_one({'_id': obj.id}, {'$set': obj.to_db_value()}, upsert=True)

    def add_original_image_to_explanation(self, user_uploaded_image: any, explanation_id: str):
        update = {"original_image": user_uploaded_image}
        self.collection.update_one({'_id': explanation_id}, {'$set': update}, upsert=True)
