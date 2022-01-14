from typing import List, Dict, Tuple

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from main.database.client import get_client
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.explain.human_readable_explanation import HumanReadableExplanation
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks, get_segments

MONGO_CLIENT = get_client()


# TODO: improve it. It's not very good, because we don't distunish between images. we should find the essence of the img
def explain_using_concepts(explanation_id: str, to_be_explained_image_index: int) -> Tuple[str, str, List[str]]:
    requirement_db = ExplanationRequirementDb(MONGO_CLIENT)
    requirement = requirement_db.get_explanation_requirement(explanation_id)

    available_concepts = requirement.available_concepts
    available_concepts.sort()

    if len(available_concepts) == 0:
        RuntimeError("Explanation can not be provided, because we can not use any concepts")

    label_nr, nr_label = build_label_maps()
    nr_feature = build_feature_names(available_concepts)

    training_data, training_labels, testing_data, testing_labels = [], [], [], []

    for index, (label, pic, mask) in enumerate(zip(get_labels(), get_images(), get_masks())):
        row = get_training_row(available_concepts, pic, mask)
        label_as_nr = label_nr[label]

        if index == to_be_explained_image_index:
            testing_data.append(row.tolist())
            testing_labels.append(np.array([label_as_nr]))
        else:
            training_labels.append(np.array([label_as_nr]))
            training_data.append(row)

    clf = train_decision_tree(np.array(training_data), np.array(training_labels))
    hre = HumanReadableExplanation(nr_label=nr_label, nr_feature=nr_feature, estimator=clf)
    return hre.human_readable_explanation(testing_data, testing_labels)


def get_training_row(available_concepts, pic, mask) -> np.array:
    row = np.zeros(len(available_concepts))
    segss, seg_class = get_segments(np.array(pic), mask, threshold=0.005)
    for index, el in enumerate(available_concepts):
        if el in seg_class:
            row[index] = 1.0
    return row


def train_decision_tree(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    return clf


def build_label_maps() -> Tuple[Dict[str, int], Dict[int, str]]:
    i = 0
    label_nr, nr_label = {}, {}
    for label in get_labels():
        if label not in label_nr:
            label_nr[label] = i
        nr_label[i] = label
        i += 1

    return label_nr, nr_label


def build_feature_names(features: List[str]) -> Dict[int, str]:
    return {i: features for i, feature in enumerate(features)}
