from typing import List, Dict
from sklearn import tree
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
        thresholds = self.estimator.tree_.threshold
        node_indicator = self.estimator.decision_path(x_test)
        leave_id = self.estimator.apply(x_test)

        sample_id = 0
        node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                            node_indicator.indptr[sample_id + 1]]

        explanations = []

        for node_id in node_index:
            if leave_id[sample_id] == node_id:
                readable_node = self.label_encoder.inverse_transform([y_test])[0]
                exp = "leaf node: {}".format(readable_node)
            else:
                if x_test[sample_id][features[node_id]] <= thresholds[node_id]:
                    threshold_sign = "<="
                else:
                    threshold_sign = ">"

                readable_feature = self.feature_encoder.inverse_transform([features[node_id]])[0]

                # wall [1.0] >= 0.5
                exp = "{}[{}] {} {}".format(
                    readable_feature,
                    x_test[sample_id][features[node_id]],
                    threshold_sign,
                    thresholds[node_id]
                )

            explanations.append(exp)

        true_label_message = "True label for this image: {}".format(
            self.label_encoder.inverse_transform(y_true)[0]
        )
        predicted_label_message = "Predicted label for this image: {}".format(
            self.label_encoder.inverse_transform([y_test])[0]
        )

        # Draw graph
        plain_text_tree = tree.export_text(self.estimator)

        return HumanReadableExplanation(
            true_label=true_label_message,
            predicted_label=predicted_label_message,
            plain_text=self.format_plain_text_tree(plain_text_tree),
            explanations=explanations
        ).to_db_format()

    def format_plain_text_tree(self, plain_tree) -> List[str]:
        as_array = []
        sorted_nr_feature = list(self.feature_encoder.transform(self.feature_encoder.classes_))
        sorted_nr_label = list(self.label_encoder.transform(self.label_encoder.classes_))

        # sorting is needed to prevent partial replacement
        sorted_nr_feature.sort(reverse=True)
        sorted_nr_label.sort(reverse=True)

        for row in plain_tree.split("\n"):
            formatted_row = row
            for feature_nr in sorted_nr_feature:
                formatted_row = formatted_row.replace("feature_{}".format(feature_nr),
                                                      self.feature_encoder.inverse_transform([feature_nr])[0])
            for label_nr in sorted_nr_label:
                formatted_row = formatted_row.replace("class: {}".format(label_nr),
                                                      "class: {}".format(
                                                          self.label_encoder.inverse_transform([label_nr])[0]))

            as_array.append(formatted_row)
        return as_array


class HumanReadableExplanation:
    def __init__(self,
                 true_label: str,
                 predicted_label: str,
                 plain_text: any,
                 explanations: List[str]):
        self.true_label = true_label
        self.predicted_label = predicted_label
        self.plain_text = plain_text
        self.explanations = explanations

    def to_db_format(self) -> Dict[str, any]:
        return {
            "trueLabel": self.true_label,
            "predictedLabel": self.predicted_label,
            "explanations": self.explanations,
            "plainTextTree": self.plain_text
        }