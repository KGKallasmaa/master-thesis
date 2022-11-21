import { ExplainableHeader } from "../common/header";
import { Col, Row } from "antd";
import { CurrentImage, OriginalImage } from "../concepts/current_image";
import { useState } from "react";
import ExplanationTypeChoiceStep from "./explaination_type_choice";
import InitalConceptsStep from "./inital_concepts";
import DesisionTreeExplanation from "../explain/desision_tree_explanation";
import CounterFactualExplanation from "../explain/counterfactual_explanation";

const explanationStep_TitelAndDescription = {
  inital_concepts: {
    title: "Select some concepts",
    description: "Select concepts that you think are important for the image.",
  },
  choose_explanation_type: {
    title: "Choose what kind of explanation you want",
    description:
      "Currently we're offering two types of explanations. Choose one of them.",
  },
  desision_tree: {
    title: "Decision Tree Explanation",
    description: "This is a decision tree explanation",
  },
  counter_factual: {
    title: "Counterfactual Explanation",
    description: "This is a counterfactual explanation",
  },
};

export default function ExplainTask(index: number) {
  if (typeof index !== "number") {
    return <div>Invalid index</div>;
  }
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
  const explanationChoiceStepIsVisible = !["", "inital_concepts"].includes(
    explanationStep
  );

  const handleSelect = (choice: string) => {
    setExplanationStep(choice);
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
          {explanationStep === "inital_concepts" && (
            <InitalConceptsStep
              onComplete={() => setExplanationStep("choose_explanation_type")}
              index={index}
            />
          )}
          {explanationChoiceStepIsVisible && (
            <ExplanationTypeChoiceStep
              onComplete={(choice) => handleSelect(choice)}
            />
          )}
          {explanationStep === "desision_tree" && (
            <DesisionTreeExplanation index={index} />
          )}
          {explanationStep === "counterfactual" && (
            <CounterFactualExplanation index={index} />
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
