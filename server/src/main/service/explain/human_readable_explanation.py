from typing import List, Tuple


class HumanReadableExplanation:
    def __init__(self, nr_label, nr_feature, estimator):
        self.nr_label = nr_label
        self.nr_feature = nr_feature
        self.estimator = estimator

    def human_readable_explanation(self, x_test, y_test) -> Tuple[str, str, List[str]]:

        feature = self.estimator.tree_.feature
        threshold = self.estimator.tree_.threshold

        node_indicator = self.estimator.decision_path(x_test)
        leave_id = self.estimator.apply(x_test)
        sample_id = 0
        node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                            node_indicator.indptr[sample_id + 1]]

        explanations = []
        print(x_test,flush=True)
        for key, value in self.nr_label.items():
            print("key:{} label:{}".format(key, value), flush=True)

        for node_id in node_index:
            if leave_id[sample_id] == node_id:
                print("my_key {}".format(leave_id[sample_id]),flush=True)
                print(explanations,flush=True)
                readable_nr = self.nr_label[leave_id[sample_id]]
                exp = "leaf node {} reached".format(readable_nr)
            else:
                if x_test[sample_id][feature[node_id]] <= threshold[node_id]:
                    threshold_sign = "<="
                else:
                    threshold_sign = ">"

                # wall [1.0] >= 0.5
                exp = "{}[{}] {} {}".format(
                    self.nr_feature[feature[node_id]],
                    x_test[sample_id][feature[node_id]],
                    threshold_sign,
                    threshold[node_id]
                )

            explanations.append(exp)

        true_label_message = "True label for this image: {}".format(self.nr_label.get(y_test[0][0]))
        predicted_label_message = "Predicted label for this image: {}".format(self.nr_label.get(leave_id[sample_id]))

        return true_label_message, predicted_label_message, explanations
