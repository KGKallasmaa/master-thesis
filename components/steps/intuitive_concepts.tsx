import { Button, Col, Row, Skeleton } from "antd";
import { useEffect, useState } from "react";
import { http, httpGet } from "../common/http";
import { Checkbox } from "antd";
import { getId } from "../common/storage";
import toast from "react-hot-toast";

type CenterMostConceptCheck = {
  label: string;
  value: string;
};

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

export default function IntuitiveConceptsStep({
  index,
  explanation_type,
  onComplete,
}: {
  index: number;
  explanation_type: string;
  onComplete: () => void;
}) {
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
  }, [index]);
  useEffect(() => {
    const payload = {
      labels: initallyProposedConcepts,
    };
    http("/center-most-concepts", payload)
      .then((el) => el.json())
      .then((data) => {
        const label = data.label;
        const center = {};
        center[label] = data.concepts.map((el) => {
          return {
            label: el.conceptName,
            value: (
              <CheckboxWithImage
                conceptChecked={(wasChecked) =>
                  handleConceptSelected(label, el.conceptName, wasChecked)
                }
                src={el.src}
                label={el.conceptName}
              />
            ),
          };
        });
        setCenterMostConcepts(center);
      });
  }, [initallyProposedConcepts]);

  const onChange = (label: string, checkedValues: CenterMostConceptCheck[]) => {
    // intutive concept name
    const inuitiveConceptNames = checkedValues.map((el) => el.label);

    const payload = {
      id: getId(),
      img: index,
      constraint_type: "intuitive",
      explanation_type: explanation_type,
      concepts: inuitiveConceptNames,
    };

    http("/concept-constraint", payload)
      .then((resp) => {})
      .catch((err) => {
        toast.error(err);
      });
  };
  useEffect(() => {
    const payload = {
      id: getId(),
      img: index,
      constraint_type: "intuitive",
      explanation_type,
      concepts: chosenIntuitiveConcepts,
    };

    // TODO: add it to backend
    http("/intuitive-concept-constraint", payload)
      .then((resp) => {})
      .catch((err) => {
        toast.error(err);
      });
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
        <Button type="primary" onClick={() => onComplete}>
          Finish
        </Button>
      </div>
    </>
  );
}
