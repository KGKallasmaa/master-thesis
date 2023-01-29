import { Button, Skeleton } from "antd";
import { useEffect, useState } from "react";
import { http, httpGet } from "../common/http";
import { Checkbox } from "antd";
import { getId } from "../common/storage";
import { ConceptCard } from "../common/card";
import toast from "react-hot-toast";

type CenterMostConceptCheck = {
  label: string;
  value: string;
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
  const [isLoading, setIsLoading] = useState(true);

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
              <ConceptCard
                title={el.conceptName}
                imageBase64={el.src}
                imageWidth={200}
                onSelected={null}
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

  if (isLoading) {
    return <Skeleton active />;
  }

  return (
    <>
      {Object.keys(centerMostConcepts).map((el) => {
        return (
          <Checkbox.Group
            options={centerMostConcepts[el]}
            onChange={(checkedValues) => onChange(el, checkedValues)}
          />
        );
      })}
      <div>
        <Button type="primary" onClick={() => onComplete}>
          Finish
        </Button>
      </div>
    </>
  );
}
