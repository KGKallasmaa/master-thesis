import { ExplainableHeader } from "../common/header";
import { Col, Row } from "antd";
import { CurrentImage, OriginalImage } from "./current_image";
import CenterConcepts from "./center_concepts";

export default function ConceptsTask(
  index: number,
  explanation_type: string,
  onComplete: () => void
) {
  const title = "Concepts";
  const description = "Please select concepts that will be used";
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
          <br />
          <CenterConcepts
            index={index}
            explanation_type={explanation_type}
            onComplete={onComplete}
          />
        </Col>
        <Col span={8} />
      </Row>
    </>
  );
}
