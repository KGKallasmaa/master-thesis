import { Button, Col, Row, Skeleton } from "antd";
import { useEffect, useState } from "react";
import { http, httpGet } from "../common/http";
import { Checkbox } from "antd";
import { getId } from "../common/storage";
import CenterMostConsept from "../explain/models/center_comost_consept";

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
  const [centerMostConcepts, setCenterMostConcepts] = useState([]);
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
      .then((data: CenterMostConsept.CenterConsept[]) => {
        data
          .filter((item) => item.concepts.length > 0)
          .forEach((item: CenterMostConsept.CenterConsept, index: any) => {
            const label = item.label;
            const concepts = item.concepts.map((concept) => {
              const conceptName = concept.name;
              return concept.examples.map((example) => {
                return {
                  label,
                  value: (
                    <CheckboxWithImage
                      conceptChecked={(wasChecked: boolean) =>
                        handleConceptSelected(label, conceptName, wasChecked)
                      }
                      src={example.src}
                      label={conceptName}
                    />
                  ),
                };
              });
            });
            setCenterMostConcepts(concepts);
          });
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
      {centerMostConcepts.map((el, index) => {
        return <Checkbox.Group key={index} options={el} />;
      })}

      <h1>size {centerMostConcepts.length}</h1>

      <div>
        <Button type="primary" onClick={onComplete}>
          Finish
        </Button>
      </div>
    </>
  );
}

const CheckboxWithImage = ({ src, label, conceptChecked }) => {
  alert("Hi");
  const [checked, setChecked] = useState(false);
  const handleChange = (e) => {
    conceptChecked(!checked);
    setChecked(e.target.checked);
    conceptChecked();
  };
  const imgSrc = `data:image/jpeg;base64,${src}`;
  console.log(imgSrc);
  return (
    <Row align="middle">
      <Col span={4}>
        <Checkbox checked={checked} onChange={handleChange} />
      </Col>
      <Col span={8}>
        <img src={imgSrc} />
      </Col>
      <Col span={12}>
        <p>{label}</p>
      </Col>
    </Row>
  );
};
