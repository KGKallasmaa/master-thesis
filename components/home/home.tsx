import Link from "next/link";
import { Col, Row } from "antd";

export default function Home() {
  return (
    <>
      <br />
      <Row>
        <Col span={8} />
        <Col span={8}>
          <h1>Explainable AI tool</h1>
          <p>This tool is used to improve machine learning</p>
        </Col>
        <Col span={8} />
      </Row>
      <br />
      <Row>
        <Col span={8} />
        <Col span={8}>
          <ul>
            <li>
              <Link href="/batch">
                <a>Batch association</a>
              </Link>
            </li>
            <li>
              <Link href="/label">
                <a>Labeling</a>
              </Link>
            </li>
            <li>
              <Link href="/upload">
                <a>Uploading</a>
              </Link>
            </li>
          </ul>
        </Col>
        <Col span={8} />
      </Row>
    </>
  );
}
