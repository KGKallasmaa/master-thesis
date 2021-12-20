from typing import List

from main.database.client import get_client
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks, get_segments
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

MONGO_CLIENT = get_client()


# TODO: improve it. It's not very good, because we don't distunish between images. we should find the essence of the img
def explain_using_concepts(id: str, img_index: int) -> List[any]:
    requirement_db = ExplanationRequirementDb(MONGO_CLIENT)
    requirement = requirement_db.get_explanation_requirement(id)

    available_concepts = requirement.get("available_concepts", [])
    available_concepts.sort()

    if len(available_concepts) == 0:
        print("Explanation can not be provided, because we can not use any concepts")
        return []

    my_label = get_labels()[img_index]

    training_data = []
    training_labels = []
    pred_data = []

    index = 0
    for label, pic, mask in zip(get_labels(), get_images(), get_masks()):
        row = get_training_row(available_concepts, pic, mask)
        training_labels.append(np.array(label))
        training_data.append(row)
        if index == img_index:
            pred_data.append(row)
        index += 1

    clf = train_decision_tree(np.array(training_data), np.array(training_labels))
    return explain(clf, [pred_data])


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


def explain(estimator, X_test):
    results = []

    n_nodes = estimator.tree_.node_count
    children_left = estimator.tree_.children_left
    children_right = estimator.tree_.children_right
    feature = estimator.tree_.feature
    threshold = estimator.tree_.threshold

    # The tree structure can be traversed to compute various properties such
    # as the depth of each node and whether or not it is a leaf.
    node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
    is_leaves = np.zeros(shape=n_nodes, dtype=bool)
    stack = [(0, -1)]  # seed is the root node id and its parent depth
    while len(stack) > 0:
        node_id, parent_depth = stack.pop()
        node_depth[node_id] = parent_depth + 1

        # If we have a test node
        if children_left[node_id] != children_right[node_id]:
            stack.append((children_left[node_id], parent_depth + 1))
            stack.append((children_right[node_id], parent_depth + 1))
        else:
            is_leaves[node_id] = True

    node_indicator = estimator.decision_path(X_test)
    leave_id = estimator.apply(X_test)
    sample_id = 0
    node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                        node_indicator.indptr[sample_id + 1]]

    for node_id in node_index:
        if leave_id[sample_id] == node_id:
            exp = "leaf node {} reached, no decision here".format(leave_id[sample_id])
        else:
            if X_test[sample_id, feature[node_id]] <= threshold[node_id]:
                threshold_sign = "<="
            else:
                threshold_sign = ">"
            exp = "decision id node {} : (X[{}, {}] (= {}) {} {})".format(
                node_id,
                sample_id,
                feature[node_id],
                X_test[sample_id, feature[node_id]],  # <-- changed i to sample_id
                threshold_sign,
                threshold[node_id]
            )
        results.append(exp)

    return results
