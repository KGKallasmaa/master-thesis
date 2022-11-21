from typing import List, Dict

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing

from main.database.closest_labels import ClosestLabelsDb
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.explain.human_readable_explanation import HumanReadableExplanationService
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks, get_segments

requirement_db = ExplanationRequirementDb()
closest_label_db = ClosestLabelsDb()


# TODO: improve it. It's not very good, because we don't distunish between images. we should find the essence of the img
def explain_using_decision_tree(explanation_id: str, to_be_explained_image_index: int) -> Dict[str, any]:
    decision_tree_concepts = to_be_used_concepts(explanation_id)
    closest = closest_label_db.get_by_image_id(to_be_explained_image_index)
    valid_labels = [closest.label] + closest.closest

    # ["office","beach","mountain"] office = 1, beach = 2
    label_encoder = encode_categorical_values(get_labels())
    # [0,0,0,0]  [1,1,0,0]  [0,0,0,0]
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

    clf = train_decision_tree(np.array(training_data), np.array(training_labels))
    predictions = clf.predict(testing_data)

    hre = HumanReadableExplanationService(label_encoder=label_encoder,
                                          feature_encoder=feature_encoder,
                                          estimator=clf)
    return hre.human_readable_explanation(x_test=testing_data,
                                          y_test=predictions,
                                          y_true=testing_labels)


def get_training_row(user_selected_concepts: List[str], pic, mask) -> np.array:
    row = np.zeros(len(user_selected_concepts))
    pic_as_array = np.array(pic)
    segss, seg_class = get_segments(pic_as_array, mask, threshold=0.005)
    for index, el in enumerate(user_selected_concepts):
        if el in seg_class:
            segment = segss[seg_class.index(el)]
            row[index] = get_segment_relative_size(segment, pic_as_array)
    return row


def train_decision_tree(x, y) -> DecisionTreeClassifier:
    x_train,_, y_train, _ = train_test_split(x, y, test_size=0.1, random_state=0)
    clf = DecisionTreeClassifier()
    clf.fit(x_train, y_train)
    return clf


def encode_categorical_values(values: List[str]) -> preprocessing.LabelEncoder:
    le = preprocessing.LabelEncoder()
    le.fit(values)
    return le


def get_segment_relative_size(segment: np.array, picture: np.array) -> float:
    segment_area = float(segment.shape[0] * segment.shape[1])
    picture_area = float(picture.shape[0] * picture.shape[1])
    return round(segment_area / picture_area, 2)


# TODO: fix this
def to_be_used_concepts(explanation_id: str) -> List[str]:
    explanation_requirement = requirement_db.get_explanation_requirement(explanation_id)
    used_concepts = explanation_requirement.constraints.initially_proposed_concepts
    if len(used_concepts) == 0:
        raise RuntimeError("Explanation can not be provided, because we can not use any concepts")
    used_concepts.sort()
    return used_concepts
