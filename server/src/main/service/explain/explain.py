from typing import List

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from main.database.client import get_client
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks, get_segments

MONGO_CLIENT = get_client()


# TODO: improve it. It's not very good, because we don't distunish between images. we should find the essence of the img
def explain_using_concepts(id: str, img_index: int) -> List[any]:
    requirement_db = ExplanationRequirementDb(MONGO_CLIENT)
    requirement = requirement_db.get_explanation_requirement(id)
    if len(requirement.available_concepts) == 0:
        print("Explanation can not be provided, because we can not use any concepts")
        return []
    requirement.available_concepts.sort()

    labels = get_labels()
    my_label = labels[img_index]

    training_data = []
    training_labels = []

    prediction_data = []

    for index, label, pic, mask in enumerate(zip(labels, get_images(), get_masks())):
        if label != my_label:
            continue
        training_labels.append(label)
        row = get_training_row(requirement, pic, mask)
        if img_index == index:
            prediction_data = [row]
        else:
            training_data.append(row)

    clf = train_decision_tree(np.array(training_data), np.array(labels))

    return clf.decision_path(np.array(prediction_data))


def get_training_row(requirement, pic, mask) -> np.array:
    row = np.zeros(len(requirement.available_concepts))
    segss, seg_class = get_segments(np.array(pic), mask, threshold=0.005)
    for index, el in enumerate(requirement.available_concepts):
        if el in seg_class:
            row[index] = 1.0
    return row


def train_decision_tree(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    return clf
