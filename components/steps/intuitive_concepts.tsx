import { Button, Col, Row, Skeleton } from "antd";
import { useEffect, useState } from "react";
import { http, httpGet } from "../common/http";
import { Checkbox } from "antd";
import { getId } from "../common/storage";

export default function IntuitiveConceptsStep({
  index,
  explanation_type,
  onComplete,
}: {
  index: number;
  explanation_type: string;
  onComplete: () => void;
}) {
  console.count("IntuitiveConceptsStep");
  const [centerMostConcepts, setCenterMostConcepts] = useState({});
  const [initallyProposedConcepts, setInitallyProposedConcepts] = useState<
    string[]
  >([]);
  const [chosenIntuitiveConcepts, setChosenIntuitiveConcepts] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  const handleConceptSelected = (
    label: string,
    concept: string,
    wasChecked: boolean
  ) => {
    let currentValues = chosenIntuitiveConcepts[label];
    if (!currentValues) {
      currentValues = [];
    }
    if (wasChecked) {
      currentValues.push(concept);
    } else {
      currentValues = currentValues.filter((el: string) => el !== concept);
    }
    setChosenIntuitiveConcepts({
      ...chosenIntuitiveConcepts,
      [label]: currentValues,
    });
  };

  useEffect(() => {
    alert("IntuitiveConceptsStep useEffect");
    httpGet(`/all-constraints/${getId()}`)
      .then((el) => el.json())
      .then((data) => {
        const initallyProposedConcepts = data["initially_proposed_concepts"];
        setInitallyProposedConcepts(initallyProposedConcepts);
      })
      .catch((err) => {
        console.log(err);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);
  useEffect(() => {
    if (initallyProposedConcepts.length === 0) {
      return;
    }
    const payload = {
      labels: initallyProposedConcepts,
    };

    http("/center-most-concepts", payload)
      .then((el) => el.json())
      .then((data) => {
        const payload = {};

        data.forEach(
          (
            item: { label: any; center: { conceptName: string; src: any }[] },
            index: any
          ) => {
            const label = item.label;
            payload[label] = item.center.map(
              (el: { conceptName: string; src: any }) => {
                return {
                  label: el.conceptName,
                  value: (
                    <CheckboxWithImage
                      conceptChecked={(wasChecked: boolean) =>
                        handleConceptSelected(label, el.conceptName, wasChecked)
                      }
                      src={el.src}
                      label={el.conceptName}
                    />
                  ),
                };
              }
            );
          }
        );
        setCenterMostConcepts(payload);
      });
  }, [initallyProposedConcepts]);

  useEffect(() => {
    /*
    const payload = {
      id: getId(),
      img: index,
      constraint_type: "intuitive",
      explanation_type,
      concepts: chosenIntuitiveConcepts,
    };

    // TODO: add it to backend
    http("/concept-constraint", payload)
      .then((resp) => {})
      .catch((err) => {
        console.log(err);
        //  toast.error(err);
      });
      */
  }, [chosenIntuitiveConcepts]);

  if (isLoading) {
    return <Skeleton active />;
  }

  return (
    <>
      {Object.keys(centerMostConcepts).map((el) => {
        return <Checkbox.Group options={centerMostConcepts[el]} />;
      })}
      <div>
        <Button type="primary" onClick={onComplete}>
          Finish
        </Button>
      </div>
    </>
  );
}

const CheckboxWithImage = ({ src, label, conceptChecked }) => {
  const [checked, setChecked] = useState(false);
  const handleChange = (e) => {
    conceptChecked(!checked);
    setChecked(e.target.checked);
    conceptChecked();
  };
  return (
    <Row align="middle">
      <Col span={4}>
        <Checkbox checked={checked} onChange={handleChange} />
      </Col>
      <Col span={8}>
        <img src={src} />
      </Col>
      <Col span={12}>
        <p>{label}</p>
      </Col>
    </Row>
  );
};
