from typing import List
from main.models.decision_tree_explanation_response import DecisionTreeExplanationResponse
from main.service.explain.common import encode_categorical_values, get_training_row, train_and_test_decision_tree
from main.service.explain.human_readable_explanation import HumanReadableExplanationService
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks
import numpy as np


def explain_using_decision_tree(to_be_explained_image_index: int,
                                decision_tree_concepts: List[str]) -> DecisionTreeExplanationResponse:
    label_encoder = encode_categorical_values(get_labels())

    X, y = [], []
    for label, pic, mask in zip(get_labels(), get_images(), get_masks()):
        row = get_training_row(decision_tree_concepts, pic, mask)
        label_as_nr = label_encoder.transform([label])
        X.append(row)
        y.append(label_as_nr)

    clf, accuracy = train_and_test_decision_tree(np.array(X), np.array(y))

    feature_encoder = encode_categorical_values(decision_tree_concepts)

    hre = HumanReadableExplanationService(label_encoder=label_encoder,
                                          feature_encoder=feature_encoder,
                                          estimator=clf)

    explanation = hre.human_readable_explanation(x_test=[X[to_be_explained_image_index]],
                                                 y_test=clf.predict([X[to_be_explained_image_index]]),
                                                 y_true=[y[to_be_explained_image_index]])

    return DecisionTreeExplanationResponse(explanation=explanation,
                                           model=clf,
                                           label_encoder=label_encoder,
                                           feature_encoder=feature_encoder,
                                           accuracy=accuracy,
                                           X=X,
                                           y=y)
