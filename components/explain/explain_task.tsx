import { ExplainableHeader } from "../common/header";
import { Col, Row } from "antd";
import { CurrentImage, OriginalImage } from "../concepts/current_image";
import CounterFactualExplanation from "./counterfactual_explanation";
import DesisionTreeExplanation from "./desision_tree_explanation";
import { Button } from "antd";
import { useState } from "react";

const explainTypeMessageMap = {
  desision_tree: "Explaining this image using a decision tree",
  counter_factual: "Explain this image using counter factuals",
};
const explainTypeButtonTextMap = {
  desision_tree: "Counterfactual Explanation",
  counter_factual: "Decision Tree Explanation",
};
const explanationStep_TitelAndDescription = {
  inital_concepts: {
    title: "Step 1: Select some concepts",
    description: "Select concepts that you think are important for the image.",
  },
};

export default function ExplainTask(index: number) {
  const [explanationStep, setExplanationStep] = useState("inital_concepts");
  const { title, description } =
    explanationStep_TitelAndDescription[explanationStep];
  //  const description = explainTypeMessageMap[explanation_type];
  //  const changeExplanationButtonText =
  //  explainTypeButtonTextMap[explanation_type];

  /*
  const handleStepChange = () => {
    if (explanation_type === "desision_tree") {
      window.location.replace(`/explain/${index}/counter_factual`);
    } else {
      window.location.replace(`/explain/${index}/desision_tree`);
    }
  };
  */
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
          {explanationStep === "inital_concepts" && (
            <DesisionTreeExplanation index={index} />
          )}
        </Col>
        <Col span={8} />
      </Row>
    </>
  );
}
/*
 <Button onClick={handleStepChange} type="primary">
            {changeExplanationButtonText}
          </Button>
          */
