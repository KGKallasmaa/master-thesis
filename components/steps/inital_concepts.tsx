import { useEffect, useState } from "react";
import { http } from "../common/http";
import { Button, Row, Skeleton } from "antd";
import { getId } from "../common/storage";
import Tags from "../common/tags";

// TODO: use this https://ant.design/components/select
export default function InitialConceptsStep({
  index,
  onComplete,
}: {
  index: number;
  onComplete: () => void;
}) {
  const [initalConcepts, setInitalConcepts] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedConcepts, setSelectedConcepts] = useState<string[]>([]);
  const [settingIsCompleted, setSettingIsCompleted] = useState(false);

  useEffect(() => {
    if (typeof index !== "number") {
      return;
    }
    if (!index) {
      return;
    }
    const payload = { img: index };
    console.log(payload);

    http("/most-popular-concepts", payload)
      .then((el) => el.json())
      .then((data) => {
        setInitalConcepts(data.concepts);
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
      constraint_type: "initially_proposed_concepts",
      concepts: selectedConcepts,
    };
    http("/concept-constraint", payload)
      .then((el) => el.json())
      .then(() => {})
      .catch(() => {})
      .finally(() => {
        onComplete();
      });
  }, [selectedConcepts, settingIsCompleted]);

  if (isLoading) {
    return <Skeleton active />;
  }

  function handleConcepClick(name: string, isSelected: boolean) {
    let currentValues = selectedConcepts;
    if (isSelected) {
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
        <p>
          {selectedConcepts.length > 0
            ? "Selected concepts (click to unselect):"
            : ""}
        </p>

        <div style={{ marginTop: 15 }}>
          <Tags
            color={"blue"}
            values={selectedConcepts}
            onClick={(value) => handleConcepClick(value, false)}
          />
        </div>
      </Row>
      <Row>
        <p>
          {initalConcepts.length - selectedConcepts.length > 0
            ? "Available concepts (click to select):"
            : ""}
        </p>

        <div style={{ marginTop: 15 }}>
          <Tags
            color={"red"}
            values={initalConcepts.filter(
              (el) => !selectedConcepts.includes(el)
            )}
            onClick={(value) => handleConcepClick(value, true)}
          />
        </div>
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
