import { ExplainableHeader } from "../common/header";
import { CurrentStep, ExplainableSteps } from "../common/steps";
import { Col, Row } from "antd";
import CurrentImage from "./current_image";
import CenterConcepts from "./center_concepts";
import TriggerExplain from "../explain/trigger_explain";

export default function ConceptsTask(index: number) {
  const title = "Concepts";
  const description =
    "Please select concepts that will be used to describe this label";
  return (
    <>
      <br />
      <ExplainableHeader title={title} description={description} />
      <br />
      <ExplainableSteps step={CurrentStep.SelectConcepts} />
      <br />
      <Row>
        <Col span={8} />
        <Col span={8}>
          <CurrentImage index={index} />
          <br />
          <TriggerExplain index={index} />
          <br />
          <CenterConcepts index={index} />
        </Col>
        <Col span={8} />
      </Row>
    </>
  );
}
