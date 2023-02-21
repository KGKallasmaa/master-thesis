import { ExplainableHeader } from "../common/header";
import { Col, Row } from "antd";
import { CurrentImage, OriginalImage } from "../concepts/current_image";
import { useState } from "react";
import ExplanationTypeChoiceStep from "./explaination_type_choice";
import InitalConceptsStep from "./inital_concepts";
import DecisionTreeExplanation from "../explain/decision_tree_explanation";
import CounterFactualExplanation from "../explain/counterfactual_explanation";
import PerformanceMetrics from "../performace/performace";
import HealthCheck from "../common/health_check";

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
  intuitive_concepts_decision_tree: {
    title: "Select some intuitive concepts for the decision tree",
    description:
      "Please address the intutive of these concepts to your decision tree explanation",
  },
  intuitive_concepts_counterfactual: {
    title: "Select some intuitive concepts for the counterfactual",
    description:
      "Please address the intutive of these concepts to your counterfactual explanation",
  },

  decision_tree: {
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

  const showPerformanceMetrics = ["decision_tree", "counterfactual"].includes(
    explanationStep
  );

  return (
    <>
      <br />
      <HealthCheck />
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
          {explanationStep === "choose_explanation_type" && (
            <>
              <ExplanationTypeChoiceStep
                onComplete={(choice) => setExplanationStep(choice)}
              />
              <br />
              <br />
            </>
          )}

          {explanationStep === "decision_tree" && (
            <DecisionTreeExplanation index={index} />
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
