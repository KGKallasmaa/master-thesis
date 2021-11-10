import { Col, Row } from "antd";
import { ConceptCard } from "../common/card";
import { useEffect, useState } from "react";
import { http } from "../common/http";

interface BatchSelectProps {
  label: string;
  model: string;
  dataset: string;
}

export function BatchSelect(props: BatchSelectProps) {
  const { model, dataset, label } = props;

  const [images, setImages] = useState([]);

  useEffect(() => {
    const payload = {
      label: label,
    };
    http("/label-all-images", payload)
      .then((el) => el.json())
      .then((data) => {
        setImages(data.results);
      });
  }, [label]);

  function handleConceptIsRelevant(name: string, decision: boolean) {}

  return (
    <>
      <h3>Correct images</h3>
      <p>
        Select images that match label: <b>{label}</b>
      </p>
      <br />
      <Row>
        {images?.map((el, i) => (
          <Col
            key={el.index}
            span={8}
            style={{ marginRight: 50, marginBottom: 20 }}
          >
            <ConceptCard
              imageBase64={el.src}
              imageWidth={200}
              onSelected={handleConceptIsRelevant}
            />
          </Col>
        ))}
      </Row>
    </>
  );
}
