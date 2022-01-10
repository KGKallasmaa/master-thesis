from typing import List, Dict, Tuple

from main.database.client import get_client
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks, get_segments
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

MONGO_CLIENT = get_client()


# TODO: improve it. It's not very good, because we don't distunish between images. we should find the essence of the img
def explain_using_concepts(id: str, img_index: int) -> List[any]:
    requirement_db = ExplanationRequirementDb(MONGO_CLIENT)
    requirement = requirement_db.get_explanation_requirement(id)

    available_concepts = requirement.available_concepts
    available_concepts.sort()

    if len(available_concepts) == 0:
        print("Explanation can not be provided, because we can not use any concepts")
        return []

    label_nr, nr_label = build_label_maps()
    nr_feature = build_feature_names(available_concepts)

    training_data = []
    training_labels = []
    pred_data = []
    for index, (label, pic, mask) in enumerate(zip(get_labels(), get_images(), get_masks())):
        row = get_training_row(available_concepts, pic, mask)
        label_as_nr = label_nr[label]

        training_labels.append(np.array([label_as_nr]))
        training_data.append(row)

        if index == img_index:
            pred_data.append(row.tolist())

    clf = train_decision_tree(np.array(training_data), np.array(training_labels))
    return explain(clf, pred_data, nr_label, nr_feature)


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


def explain(estimator, X_test, nr_label, nr_feature):
    """
    TODO: we should not have explaaints where labels are numbers
    """
    results = []

    feature = estimator.tree_.feature
    threshold = estimator.tree_.threshold

    node_indicator = estimator.decision_path(X_test)
    leave_id = estimator.apply(X_test)
    sample_id = 0
    node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                        node_indicator.indptr[sample_id + 1]]

    for node_id in node_index:
        if leave_id[sample_id] == node_id:
            readable_nr = nr_feature[leave_id[sample_id]]
            exp = "leaf node {} reached, no decision here".format(readable_nr)
        else:
            if X_test[sample_id][feature[node_id]] <= threshold[node_id]:
                threshold_sign = "<="
            else:
                threshold_sign = ">"
            exp = "decision id node {} : (X[{}, {}] (= {}) {} {})".format(
                node_id,
                sample_id,
                feature[node_id],
                X_test[sample_id][feature[node_id]],
                threshold_sign,
                threshold[node_id]
            )
        results.append(exp)

    return results


def build_label_maps() -> Tuple[Dict[str, int], Dict[int, str]]:
    i = 0
    label_nr = {}
    nr_label = {}
    for label in get_labels():
        if label not in label_nr:
            label_nr[label] = i
            nr_label[i] = label
            i += 1
    return label_nr, nr_label


def build_feature_names(features: List[str]) -> Dict[int, str]:
    results = {}
    for i, feature in enumerate(features):
        results[i] = feature
    return results
