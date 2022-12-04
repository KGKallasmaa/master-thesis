from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import numpy as np


class DecisionTreeExplanationResponse:
    def __init__(self, feature_encoder, label_encoder, model, explanation, X, y):
        self.feature_encoder = feature_encoder
        self.label_encoder = label_encoder
        self.model = model
        self.explanation = explanation
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=10, random_state=42)
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        # [ 9 23 18  3  3  3  3  3  6 30]
        self.predictions = model.predict(X_test)
        # TODO: we can probably get rid of this
        self.transformed_predictions = label_encoder.inverse_transform(self.predictions)
        self.transformed_y_test = label_encoder.inverse_transform(y_test)
        self.accuracy = accuracy_score(y_test, self.predictions)
