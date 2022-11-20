import { Col, Row, Skeleton, Tag } from "antd";
import { useEffect, useState } from "react";
import { http } from "../common/http";
import { getId } from "../common/storage";
import Tags from "../common/tags";

type ConceptsManagerProps = {
  index: number;
  explanation_type: string;
  onChangeCompleted: () => void;
};

export default function ConceptsManager(props: ConceptsManagerProps) {
  const { index, explanation_type, onChangeCompleted } = props;

  const [currentlyUsedConcepts, setCurrentlyUsedConcepts] = useState<string[]>(
    []
  );
  const [availableToBeChosenConcepts, setAvailableToBeChosenConcepts] =
    useState<string[]>([]);
  const [isLoading, setLoading] = useState(true);

  useEffect(() => {
    const payload = {
      id: getId(),
      img: index,
      explanationType: explanation_type,
    };
    http("/explanation-concepts", payload)
      .then((el) => el.json())
      .then((data) => {
        setCurrentlyUsedConcepts(data.usedConcepts);
        setAvailableToBeChosenConcepts(data.availableToBeChosenConcepts);
      })
      .catch((err) => {
        console.error(err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [props.index, props.explanation_type]);

  const handeleConceptChange = (conceptName: string, isAdding: boolean) => {
    const payload = {
      id: getId(),
      img: index,
      conceptName,
      isAdding,
    };
    http("/explanation-concepts-change", payload).finally(() => {
      setLoading(false);
      onChangeCompleted();
    });
  };

  if (isLoading) {
    return <Skeleton active />;
  }

  return (
    <>
      <Row>
        <p>
          {currentlyUsedConcepts.length > 0
            ? "Selected concepts (click to unselect):"
            : ""}
        </p>
        <div style={{ marginTop: 15 }}>
          <Tags
            color={"blue"}
            values={currentlyUsedConcepts}
            onClick={(value) => handeleConceptChange(value, false)}
          />
        </div>
      </Row>
      <Row>
        <p>
          {availableToBeChosenConcepts.length > 0
            ? "Available concepts (click to select):"
            : ""}
        </p>

        <div style={{ marginTop: 15 }}>
          <Tags
            color={"red"}
            values={availableToBeChosenConcepts}
            onClick={(value) => handeleConceptChange(value, true)}
          />
        </div>
      </Row>
    </>
  );
}
