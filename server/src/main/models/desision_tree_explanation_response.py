from typing import Tuple

from sklearn.metrics import accuracy_score


class DecisionTreeExplanationResponse:
    def __init__(self, feature_encoder, label_encoder, model, explanation, X, y, allowed_labels):
        self.feature_encoder = feature_encoder
        self.label_encoder = label_encoder
        self.model = model
        self.explanation = explanation
        X_train, X_test, y_train, y_test = non_shuffling_train_test_split(X, y, test_size=0.1)

        # [ 9 23 18  3  3  3  3  3  6 30]
        predictions = model.predict(X_test)
        all_predictions = model.predict(X)
        self.transformed_predictions = label_encoder.inverse_transform(predictions)
        self.transformed_all_predictions = label_encoder.inverse_transform(all_predictions)
        self.transformed_y_test = label_encoder.inverse_transform(y_test)
        self.accuracy = accuracy_score(y_test, predictions)
        self.allowed_labels = allowed_labels


def non_shuffling_train_test_split(X, y, test_size=0.1) -> Tuple[any, any, any, any]:
    X_train, X_test, y_train, y_test = [], [], [], []

    last_x_index = len(X) * test_size

    for i in range(len(X)):
        if i >= last_x_index:
            X_train.append(X[i])
            y_train.append(y[i])
        else:
            X_test.append(X[i])
            y_test.append(y[i])

    return X_train, X_test, y_train, y_test
