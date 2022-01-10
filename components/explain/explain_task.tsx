import { ExplainableHeader } from "../common/header";
import { CurrentStep, ExplainableSteps } from "../common/steps";
import { Col, Row } from "antd";
import { getId } from "../common/storage";
import CurrentImage from "../concepts/current_image";

export default function ExplainTask(index: number) {
  const title = "Explain";
  const description = "Explaining this image using a decision tree";
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
          <MachineLearningExplanation index={index} />
        </Col>
        <Col span={8} />
      </Row>
    </>
  );
}
function MachineLearningExplanation(props: { index: number }) {
  const payload = {
    id: getId(),
    index: props.index,
  };
  return <b>implement ML explanation here</b>;
}
