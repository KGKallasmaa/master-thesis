import { Col, Row, Steps } from "antd";

const { Step } = Steps;

export enum CurrentStep {
  Upload,
  SelectConcepts,
    ExplainModels
}

export function ExplainableSteps(props: { step: CurrentStep }) {
  return (
    <Row>
      <Col span={2} />
      <Col span={20}>
        <Steps size="small" current={props.step}>
          <Step title="Upload image" />
          <Step title="Select concepts" />
          <Step title="Explain models" />
        </Steps>
      </Col>
      <Col span={2} />
    </Row>
  );
}
