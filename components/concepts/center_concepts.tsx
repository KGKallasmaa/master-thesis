import { useEffect, useState } from "react";
import { http } from "../common/http";
import { Button, Col, Row, Skeleton } from "antd";
import { ConceptCard } from "../common/card";
import { getId } from "../common/storage";

export default function CenterConcepts(props: {
  index: number;
  label?: string;
  explanation_type: string;
  onComplete: () => void;
}) {
  const { index, label } = props;
  const [images, setImage] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedConcepts, setSelectedConcepts] = useState<string[]>([]);
  const [settingIsCompleted, setSettingIsCompleted] = useState(false);

  useEffect(() => {
    const payload = label ? { label, index } : { index };

    http("/center-most-concepts", payload)
      .then((el) => el.json())
      .then((data) => {
        setImage(data.results);
        setIsLoading(false);
      })
      .catch(() => {
        setIsLoading(false);
      });
  }, [index]);

  useEffect(() => {
    if (selectedConcepts.length == 0 || !settingIsCompleted) {
      return;
    }
    const payload = {
      id: getId(),
      img: index,
      explanation_type: props.explanation_type,
      concepts: selectedConcepts,
    };
    http("/concept-constraint", payload)
      .then((el) => el.json())
      .then(() => {})
      .catch(() => {})
      .finally(() => {
        props.onComplete();
      });
  }, [selectedConcepts, settingIsCompleted]);

  if (isLoading) {
    return <Skeleton active />;
  }

  function handleConceptWillBeUsed(name: string, decision: boolean) {
    let currentValues = selectedConcepts;
    if (decision) {
      currentValues.push(name);
    } else {
      currentValues = removeElFromArray(currentValues, name);
    }
    currentValues = [...new Set(currentValues)];
    setSelectedConcepts(currentValues);
  }

  return (
    <>
      {selectedConcepts.length > 0 && (
        <>
          <Button
            type="primary"
            onClick={() => setSettingIsCompleted(!settingIsCompleted)}
          >
            {settingIsCompleted ? "Select more" : "Finish selecting"}
          </Button>
          <br />
          <br />
        </>
      )}
      <Row>
        <p>Selected concepts:</p>
        <br />
        <br />
        {selectedConcepts.map((el) => (
          <div key={el}>
            <p>{el},</p>
            <br />
          </div>
        ))}
      </Row>
      <Row>
        {images.map((el, i) => (
          <Col span={8} key={i} style={{ marginRight: 50, marginBottom: 20 }}>
            <ConceptCard
              key={i}
              label={el.conceptName}
              imageBase64={el.src}
              imageWidth={200}
              onSelected={handleConceptWillBeUsed}
              title={""}
            />
          </Col>
        ))}
      </Row>
    </>
  );
}

function removeElFromArray(arr: string[], value: string): string[] {
  let i = 0;
  while (i < arr.length) {
    if (arr[i] === value) {
      arr.splice(i, 1);
    } else {
      ++i;
    }
  }
  return arr;
}
