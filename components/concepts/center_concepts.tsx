import { useEffect, useState } from "react";
import { http } from "../common/http";
import { Col, Row, Skeleton } from "antd";
import { ConceptCard } from "../common/card";
import DetailedConcept from "./detail_concepts";

export default function CenterConcepts(props: { index: number }) {
  const { index } = props;
  const [images, setImage] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    http("/center-most-concepts", {})
      .then((el) => el.json())
      .then((data) => {
        setImage(data.results);
        setIsLoading(false);
      })
      .catch(() => {
        setIsLoading(false);
      });
  }, [index]);
  const [selectedConcepts, setSelectedConcepts] = useState<string[]>([]);

  function handleConceptWillBeUsed(name: string, decision: boolean) {
    if (decision == true) {
      setSelectedConcepts(selectedConcepts.concat(name));
    }
  }

  if (isLoading) return <Skeleton active />;

  return (
    <Row>
      {images.map((el, i) => (
        <Col span={8} key={i} style={{ marginRight: 50, marginBottom: 20 }}>
          <ConceptCard
            key={i}
            label={el.conceptName}
            imageBase64={el.src}
            imageWidth={200}
            onSelected={handleConceptWillBeUsed}
          />
          {selectedConcepts.includes(el.conceptName) && (
            <DetailedConcept name={el.conceptName} />
          )}
        </Col>
      ))}
    </Row>
  );
}
