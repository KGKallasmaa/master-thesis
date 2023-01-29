import { ExplainableHeader } from "../common/header";
import { Col, Row } from "antd";
import { CurrentImage, OriginalImage } from "../concepts/current_image";
import { useState } from "react";
import ExplanationTypeChoiceStep from "./explaination_type_choice";
import InitalConceptsStep from "./inital_concepts";
import DesisionTreeExplanation from "../explain/desision_tree_explanation";
import CounterFactualExplanation from "../explain/counterfactual_explanation";
import PerformanceMetrics from "../performace/performace";
import IntuitiveConceptsStep from "./intuitive_concepts";

const explanationStep_TitelAndDescription = {
  inital_concepts: {
    title: "Select some concepts",
    description: "Select concepts that you think are important for the image.",
  },
  intuitive_concepts: {
    title: "Confirm inuitive concepts",
    description:"Are those concepts inuitive to you?",
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
  counterfactual: {
    title: "Counterfactual Explanation",
    description: "This is a counterfactual explanation",
  },
};

export default function ExplainTask(index: number) {
  const [explanationStep, setExplanationStep] = useState("inital_concepts");

  const { title, description } =
    explanationStep_TitelAndDescription[explanationStep];

  const explanationChoiceStepIsVisible = !["", "inital_concepts","intuitive_concepts"].includes(
    explanationStep
  );

  const handleSelect = (choice: string) => {
    setExplanationStep(choice);
  };
  const showPerformanceMetrics = ["desision_tree", "counterfactual"].includes(
    explanationStep
  );

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
              onComplete={() => setExplanationStep("intuitive_concepts")}
              index={index}
            />
          )}
          {explanationStep === "intuitive_concepts" && (
            <IntuitiveConceptsStep
              onComplete={() => setExplanationStep("choose_explanation_type")}
              index={index}
            />
          )}
          {explanationChoiceStepIsVisible && (
            <>
              <ExplanationTypeChoiceStep
                onComplete={(choice) => handleSelect(choice)}
              />
              <br />
              <br />
            </>
          )}
          {explanationStep === "desision_tree" && (
            <DesisionTreeExplanation index={index} />
          )}
          {explanationStep === "counterfactual" && (
            <CounterFactualExplanation index={index} />
          )}
        </Col>
        <Col span={8}>
          {showPerformanceMetrics && (
            <PerformanceMetrics explanation_type={explanationStep} />
          )}
        </Col>
      </Row>
    </>
  );
}
