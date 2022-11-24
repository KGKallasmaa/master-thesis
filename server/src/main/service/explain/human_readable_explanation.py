from typing import Dict, Optional, List
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier


class HumanReadableExplanationService:
    def __init__(self,
                 label_encoder: preprocessing.LabelEncoder,
                 feature_encoder: preprocessing.LabelEncoder,
                 estimator: DecisionTreeClassifier):
        self.label_encoder = label_encoder
        self.feature_encoder = feature_encoder
        self.estimator = estimator

    def human_readable_explanation(self, x_test, y_test, y_true) -> Dict[str, any]:
        features = self.estimator.tree_.feature
        node_indicator = self.estimator.decision_path(x_test)
        leave_id = self.estimator.apply(x_test)

        sample_id = 0
        node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                            node_indicator.indptr[sample_id + 1]]

        features_present_in_explanation = []

        for node_id in node_index:
            if leave_id[sample_id] != node_id:
                readable_feature = self.feature_encoder.inverse_transform([features[node_id]])[0]
                features_present_in_explanation.append(readable_feature)

        true_label_message = f"True label for this image: {self.label_encoder.inverse_transform(y_true)[0]}"
        predicted_label_message = f"Predicted label for this image: {self.label_encoder.inverse_transform([y_test])[0]}"

        human_readable_explain = HumanReadableExplanation(
            true_label=true_label_message,
            predicted_label=predicted_label_message,
            feature_importance=self.__feature_importance(features_present_in_explanation),
        )
        return human_readable_explain.to_db_format()

    def __feature_importance(self, features_in_local_explanation: List[str]) -> List[Dict[str, float]]:
        results = {feature: {"featureName": feature, "global": importance,} for feature, importance in zip(self.feature_encoder.classes_, self.estimator.feature_importances_)}

        feature_local_score = {feature: results[feature]["global"] for feature in features_in_local_explanation}
        total_local_score = sum(feature_local_score.values())
        feature_local_score = {k: v / total_local_score for k, v in feature_local_score.items()}

        for feature_name in results:
            local_score = feature_local_score.get(feature_name, 0)
            global_score = results[feature_name]["global"]

            local_score = round(100*local_score, 2)
            global_score = round(100*global_score, 2)

            results[feature_name]["local"] = local_score
            results[feature_name]["global"] = global_score

        return sorted(list(results.values()), key=lambda x: x["local"], reverse=True)


class HumanReadableExplanation:
    def __init__(self,
                 true_label: Optional[str],
                 predicted_label: str,
                 feature_importance: List[dict[str, float]]):
        self.true_label = true_label
        self.predicted_label = predicted_label
        self.feature_importance = feature_importance

    def to_db_format(self) -> Dict[str, any]:
        payload = {
            "trueLabel": self.true_label,
            "predictedLabel": self.predicted_label,
            "featureImportance": self.feature_importance,
        }
        to_be_deleted = [key for key, value in payload.items() if value is None]
        for key in to_be_deleted:
            del payload[key]
        return payload
