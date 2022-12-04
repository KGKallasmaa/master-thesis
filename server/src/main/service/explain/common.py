from typing import List, Tuple

import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from main.service.pre_explanation.data_access import get_segments


def encode_categorical_values(values: List[str]) -> preprocessing.LabelEncoder:
    unique_values = sorted(list(set(values)))
    le = preprocessing.LabelEncoder()
    le.fit(unique_values)
    return le


def get_training_row(user_selected_concepts: List[str], pic, mask) -> np.array:
    row = np.zeros(len(user_selected_concepts))
    pic_as_array = np.array(pic)
    segss, seg_class = get_segments(pic_as_array, mask, threshold=0.005)
    for index, el in enumerate(user_selected_concepts):
        if el in seg_class:
            segment = segss[seg_class.index(el)]
            row[index] = get_segment_relative_size(segment, pic_as_array)
    return row


def train_decision_tree(x, y) -> Tuple[DecisionTreeClassifier, float]:
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=0)
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    return clf, clf.score(X_test, y_test)


def get_segment_relative_size(segment: np.array, picture: np.array) -> float:
    segment_area = float(segment.shape[0] * segment.shape[1])
    picture_area = float(picture.shape[0] * picture.shape[1])
    return round(segment_area / picture_area, 2)
