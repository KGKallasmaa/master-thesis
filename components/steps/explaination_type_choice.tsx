import { Select } from "antd";

const options = [
  {
    value: "decision_tree",
    label: "Decision Tree",
  },
  {
    value: "counterfactual",
    label: "Counterfactual",
  },
];

interface ExplanationTypeChoiceProps {
  onComplete: (choice: string) => void;
}

export default function ExplanationTypeChoiceStep(
  props: ExplanationTypeChoiceProps
) {
  return (
    <Select
      style={{ width: 200 }}
      onChange={(value) => props.onComplete(value)}
      placeholder="Select explanation type"
      options={options}
    />
  );
}
