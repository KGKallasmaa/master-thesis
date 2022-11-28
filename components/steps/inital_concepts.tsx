import { useEffect, useState } from "react";
import { http } from "../common/http";
import { Button, Col, Row, Skeleton } from "antd";
import { getId } from "../common/storage";
import toast from "react-hot-toast";
import Tags from "../common/tags";

const initalConceptConstraint = "initially_proposed_concepts";

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
      constraint_type: initalConceptConstraint,
      concepts: selectedConcepts,
    };

    http("/concept-constraint", payload)
      .then((resp) => {
        console.log(resp);
        if (resp.status === 204) {
          alert("hello");
          onComplete();
        }
      })
      .catch((err) => {
        console.log(err);
        toast.error(err);
        setSettingIsCompleted(false);
      });
  }, [selectedConcepts, settingIsCompleted]);

  if (isLoading) {
    return <Skeleton active />;
  }

  function handleConcepClick(name: string, isSelected: boolean) {
    alert("hi");
    let currentValues = selectedConcepts;
    if (isSelected) {
      currentValues.push(name);
    } else {
      currentValues = removeElFromArray(currentValues, name);
    }
    currentValues = [...new Set(currentValues)];
    setSelectedConcepts(currentValues);
  }

  function handleSelectAll() {
    const allConcepts = initalConcepts.filter(
      (el) => !selectedConcepts.includes(el)
    );
    setSelectedConcepts(allConcepts);
  }

  return (
    <>
      {selectedConcepts.length == 0 && (
        <>
          <p>Choose the concepts that will be used to explain this image.</p>
          <p>Concepts not chosen will not be used</p>
        </>
      )}

      {selectedConcepts.length > 0 && (
        <>
          <Button type="primary" onClick={() => setSettingIsCompleted(true)}>
            {settingIsCompleted ? "Select more" : "Finish selecting"}
          </Button>
          <br />
          <br />
        </>
      )}
      {selectedConcepts.length > 0 && (
        <Row>
          <Col span={24}>
            <p>Selected concepts (click to unselect):</p>
          </Col>
          <Col span={12}>
            <Button type="dashed" onClick={() => setSelectedConcepts([])}>
              Unselect all
            </Button>
          </Col>
          <Col span={24}>
            <div style={{ marginTop: 15 }}>
              <Tags
                color={"blue"}
                values={selectedConcepts}
                onClick={(value) => handleConcepClick(value, false)}
              />
            </div>
          </Col>
        </Row>
      )}
      {initalConcepts.length - selectedConcepts.length > 0 && (
        <Row>
          <Col span={24}>
            <p>Available concepts (click to select):</p>
          </Col>
          <Col span={12}>
            <Button type="primary" onClick={() => handleSelectAll()}>
              Select all
            </Button>
          </Col>
          <Col span={24}>
            <div style={{ marginTop: 15 }}>
              <Tags
                color={"red"}
                values={initalConcepts.filter(
                  (el) => !selectedConcepts.includes(el)
                )}
                onClick={(value) => handleConcepClick(value, true)}
              />
            </div>
          </Col>
        </Row>
      )}
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
