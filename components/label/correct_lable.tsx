import { Row, Col } from "antd";
import { ConceptCard } from "../common/card";
import { useEffect, useState } from "react";
import { http } from "../common/http";

interface CorrectLabelingTaskProps {
  model: string;
  dataset: string;
  label: string;
}

export function CorrectLabelingTask(props: CorrectLabelingTaskProps) {
  const { model, dataset, label } = props;

  const [image, setImage] = useState("");
  const [imageIndex, setImageIndex] = useState(-1);
  const [conceptsFromImage, setConceptsFromImage] = useState([]);

  useEffect(() => {
    const payload = {
      label: label,
    };
    http("/label-image", payload)
      .then((el) => el.json())
      .then((data) => {
        setImage(data.url);
        setImageIndex(data.index);
      });
  });
  useEffect(() => {
    const payload = {
      index: imageIndex,
    };
    http("/image-segments", payload)
      .then((el) => el.json())
      .then((data) => {
        setConceptsFromImage(data.results);
      });
  }, [imageIndex]);

  function handleCategoryIsRelevant(name: string, decision: boolean) {}

  function handleConceptIsRelevant(name: string, decision: boolean) {}

  return (
    <>
      <h3>Label image association</h3>
      <p>Can this image be associated with this concept</p>
      <Row>
        <ConceptCard
          key={label}
          label={label}
          imageBase64={image}
          imageWidth={300}
          onSelected={handleCategoryIsRelevant}
        />
      </Row>

      <br />

      <h3>Select relevant concepts</h3>
      <p>
        Please select concepts that can be associated with label <b>{label}</b>
      </p>
      <br />
      <Row>
        {conceptsFromImage?.map((el) => (
          <Col
            key={el.conceptName}
            span={8}
            style={{ marginRight: 50, marginBottom: 20 }}
          >
            <ConceptCard
              label={el.conceptName}
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
