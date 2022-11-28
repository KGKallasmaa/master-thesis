from typing import List, Dict, Tuple

import numpy as np

from main.database.closest_labels import ClosestLabelsDb
from main.database.constraint_db import ConstraintDb
from main.database.explanation_requirement import ExplanationRequirementDb
from main.models.enums import ExplanationType
from main.service.explain.common import encode_categorical_values, get_training_row, train_decision_tree
from main.service.explain.human_readable_explanation import HumanReadableExplanationService
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks


class DecisionTreeExplanationService:
    def __init__(self):
        self.requirement_db = ExplanationRequirementDb()
        self.closest_label_db = ClosestLabelsDb()
        self.constraint_db = ConstraintDb()

    def explain(self, explanation_id: str, to_be_explained_image_index: int) -> Dict[str, any]:
        concepts = self.to_be_used_concepts(explanation_id)
        feature_encoder, estimator, explanation = self.explain_using_decision_tree(to_be_explained_image_index,
                                                                                   concepts)
        self.update_used_constraints(explanation_id=explanation_id,
                                     feature_encoder=feature_encoder,
                                     estimator=estimator)
        return explanation

    def explain_using_decision_tree(self, to_be_explained_image_index: int,
                                    decision_tree_concepts: List[str]) -> Tuple[any, any, Dict[str, any]]:
        closest = self.closest_label_db.get_by_image_id(to_be_explained_image_index)
        valid_labels = [closest.label] + closest.closest

        label_encoder = encode_categorical_values(get_labels())
        feature_encoder = encode_categorical_values(decision_tree_concepts)

        training_data, training_labels, testing_data, testing_labels = [], [], [], []

        # TDO: we should not loop over every single image
        for index, (label, pic, mask) in enumerate(zip(get_labels(), get_images(), get_masks())):
            if label not in valid_labels:
                continue
            row = get_training_row(decision_tree_concepts, pic, mask)
            label_as_nr = label_encoder.transform([label])

            if index == to_be_explained_image_index:
                testing_labels.append(label_as_nr)
                testing_data.append(row)
            else:
                training_labels.append(label_as_nr)
                training_data.append(row)

        clf, accuracy = train_decision_tree(np.array(training_data), np.array(training_labels))

        predictions = clf.predict(testing_data)
        hre = HumanReadableExplanationService(label_encoder=label_encoder,
                                              feature_encoder=feature_encoder,
                                              estimator=clf)

        explanation = hre.human_readable_explanation(x_test=testing_data, y_test=predictions, y_true=testing_labels)

        return feature_encoder, clf, explanation

    def to_be_used_concepts(self, explanation_id: str) -> List[str]:
        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)
        print(constraints.to_db_value(), flush=True)
        print(constraints.most_predictive_concepts, flush=True)
        human_readable_concepts = constraints.user_selected_concepts[ExplanationType.DECISION_TREE.value]
        if len(human_readable_concepts) == 0:
            human_readable_concepts = constraints.initially_proposed_concepts
        if len(human_readable_concepts) == 0:
            raise ValueError("Decision tree explanation requires at least one concept for explanation")
        return human_readable_concepts

    def update_used_constraints(self, explanation_id: str, feature_encoder, estimator):
        feature_importance = {feature: {"featureName": feature, "local": importance} for feature, importance in
                              zip(feature_encoder.classes_, estimator.feature_importances_)}

        feature_importance = sorted(list(feature_importance.values()), key=lambda x: x["local"], reverse=True)
        most_predictive_features = [feature["featureName"] for feature in feature_importance]

        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)

        constraints.change_concept_constraint("most_predictive_concepts", ExplanationType.DECISION_TREE,
                                              most_predictive_features)

        self.constraint_db.update_constraint(constraints)
