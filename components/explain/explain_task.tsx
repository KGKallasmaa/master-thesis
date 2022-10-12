import { ExplainableHeader } from "../common/header";
import { CurrentStep, ExplainableSteps } from "../common/steps";
import { Col, Row } from "antd";
import { useState } from "react";
import { CurrentImage } from "../concepts/current_image";
import CounterFactualExplanation from "./counterfactual_explanation";
import MachineLearningExplanation from "./machine_learning_explanation";

export default function ExplainTask(index: number) {
  const title = "Explain";
  const description = "Explaining this image using a decision tree";
  const [currentStep, setCurrentStep] = useState<CurrentStep>(
    CurrentStep.ExplainModels
  );
  const [buttonText, setButtonText] = useState<string>(
    "View Counterfactual Explanation"
  );
  const handleStepChange = () => {
    if (currentStep === CurrentStep.ExplainModels) {
      setCurrentStep(CurrentStep.CounterFactualExplanation);
      setButtonText("View Decision Tree Explanation");
    } else {
      setCurrentStep(CurrentStep.ExplainModels);
      setButtonText("View Counterfactual Explanation");
    }
  };
  return (
    <>
      <br />
      <ExplainableHeader title={title} description={description} />
      <br />
      <ExplainableSteps step={currentStep} />
      <br />
      <Row>
        <Col span={8} />
        <Col span={8}>
          <CurrentImage index={index} />
          <br />
          {currentStep === CurrentStep.ExplainModels && (
            <MachineLearningExplanation index={index} />
          )}
          {currentStep === CurrentStep.CounterFactualExplanation && (
            <CounterFactualExplanation index={index} />
          )}
          <br />
          <button onClick={handleStepChange}>{buttonText}</button>
        </Col>
        <Col span={8} />
      </Row>
    </>
  );
}
