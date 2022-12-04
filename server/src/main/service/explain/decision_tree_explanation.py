from typing import List

from main.models.desision_tree_explanation_response import DecisionTreeExplanationResponse
from main.service.explain.common import encode_categorical_values, get_training_row, train_decision_tree
from main.service.explain.human_readable_explanation import HumanReadableExplanationService
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks
import numpy as np


def explain_using_decision_tree(valid_labels: List[str], to_be_explained_image_index: int,
                                decision_tree_concepts: List[str]) -> DecisionTreeExplanationResponse:
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

    clf, _ = train_decision_tree(np.array(training_data), np.array(training_labels))

    predictions = clf.predict(testing_data)
    hre = HumanReadableExplanationService(label_encoder=label_encoder,
                                          feature_encoder=feature_encoder,
                                          estimator=clf)

    explanation = hre.human_readable_explanation(x_test=testing_data, y_test=predictions, y_true=testing_labels)

    X, y = [], []
    X.extend(iter(training_data))
    X.extend(iter(testing_data))
    y.extend(iter(training_labels))
    y.extend(iter(testing_labels))

    return DecisionTreeExplanationResponse(explanation=explanation,
                                           model=clf,
                                           feature_encoder=feature_encoder,
                                           label_encoder=label_encoder,
                                           allowed_labels=valid_labels,
                                           X=X,
                                           y=y)
