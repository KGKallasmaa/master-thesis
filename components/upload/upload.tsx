import { Col, Row } from "antd";
import { UploadTask } from "./upload_task";
import { CurrentStep, ExplainableSteps } from "../common/steps";
import { ExplainableHeader } from "../common/header";

export default function Upload() {
  const title = "Upload";
  const description = "Upload the mage you would like us to explain";

  function handleSuccessfulUpload(img_index: number) {
    window.location.replace("/concepts/" + img_index);
  }

  return (
    <>
      <br />
      <ExplainableHeader title={title} description={description} />
      <br />
      <ExplainableSteps step={CurrentStep.Upload} />
      <br />
      <Row>
        <Col span={8} />
        <Col span={8}>
          <UploadTask uploadComplete={handleSuccessfulUpload} />
        </Col>
        <Col span={8} />
      </Row>
    </>
  );
}
