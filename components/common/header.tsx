import { Col, Row } from "antd";

export function ExplainableHeader(props: {
  title: string;
  description: string;
}) {
  return (
    <Row>
      <Col span={8} />
      <Col span={8}>
        <h1>{props.title}</h1>
        <br />
        <p>{props.description}</p>
      </Col>
      <Col span={8} />
    </Row>
  );
}
