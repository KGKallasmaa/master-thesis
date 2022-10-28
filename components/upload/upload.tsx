import { Col, Row } from "antd";
import { UploadTask } from "./upload_task";
import { ExplainableHeader } from "../common/header";

export default function Upload() {
  const title = "Upload";
  const description = "Upload the image you would like us to explain";

  function handleSuccessfulUpload(img_index: number) {
    window.location.replace(`/explain/${img_index}/desision_tree`);
  }

  return (
    <>
      <br />
      <ExplainableHeader title={title} description={description} />
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
