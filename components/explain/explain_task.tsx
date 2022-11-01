import { ExplainableHeader } from "../common/header";
import { Col, Row } from "antd";
import { CurrentImage, OriginalImage } from "../concepts/current_image";
import CounterFactualExplanation from "./counterfactual_explanation";
import DesisionTreeExplanation from "./desision_tree_explanation";
import { Button } from "antd";

const explainTypeMessageMap = {
  desision_tree: "Explaining this image using a decision tree",
  counter_factual: "Explain this image using counter factuals",
};
const explainTypeButtonTextMap = {
  desision_tree: "Counterfactual Explanation",
  counter_factual: "Decision Tree Explanation",
};

export default function ExplainTask(index: number, explanation_type: string) {
  const title = "Explain";
  const description = explainTypeMessageMap[explanation_type];
  const changeExplanationButtonText =
    explainTypeButtonTextMap[explanation_type];

  const handleStepChange = () => {
    if (explanation_type === "desision_tree") {
      window.location.replace(`/explain/${index}/counter_factual`);
    } else {
      window.location.replace(`/explain/${index}/desision_tree`);
    }
  };
  return (
    <>
      <br />
      <ExplainableHeader title={title} description={description} />
      <br />
      <Row>
        <Col span={8} />
        <Col span={8}>
          <CurrentImage index={index} />
          <br />
          <OriginalImage />
          <br />
          {explanation_type === "desision_tree" && (
            <DesisionTreeExplanation index={index} />
          )}
          {explanation_type === "counter_factual" && (
            <CounterFactualExplanation index={index} />
          )}
          <br />
          <br />
          <Button onClick={handleStepChange} type="primary">
            {changeExplanationButtonText}
          </Button>
        </Col>
        <Col span={8} />
      </Row>
    </>
  );
}
