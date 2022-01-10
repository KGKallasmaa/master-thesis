import { useEffect, useState } from "react";
import { http } from "../common/http";
import { Col, Row, Skeleton } from "antd";
import { ConceptCard } from "../common/card";

export default function DetailedConcept(props: { name: string }) {
  const { name } = props;
  const [images, setImage] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    http("/concept-representatives", { name: name })
      .then((el) => el.json())
      .then((data) => {
        setImage(data.results);
        setIsLoading(false);
      })
      .catch(() => {
        setIsLoading(false);
      });
  }, [name]);

  function conceptRepresentativeClicked(name: string, decision: boolean) {
    console.log("Concept representative will be used was clicked hihi");
  }

  if (isLoading) return <Skeleton active />;

  return (
    <Row>
      <p>Please review more images from this concepts</p>
      {images.map((el, i) => (
        <Col span={8} key={i} style={{ marginRight: 50, marginBottom: 20 }}>
          <ConceptCard
            key={i}
            label={el.conceptName}
            imageBase64={el.src}
            imageWidth={200}
            onSelected={conceptRepresentativeClicked}
          />
        </Col>
      ))}
    </Row>
  );
}