from typing import Tuple


class DecisionTreeExplanationResponse:
    def __init__(self,feature_encoder, label_encoder, model, explanation, X, y,accuracy):
        self.explanation = explanation
        self.feature_encoder = feature_encoder
        self.model = model
        X_train, X_test, y_train, y_test = non_shuffling_train_test_split(X, y, test_size=0.1)
        predictions = model.predict(X_test)
        self.transformed_predictions = label_encoder.inverse_transform(predictions)
        self.accuracy = accuracy


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
