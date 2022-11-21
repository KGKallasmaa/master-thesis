import { Row, Skeleton } from "antd";
import { useEffect, useState } from "react";
import { http } from "../common/http";
import { getId } from "../common/storage";
import Tags from "../common/tags";

type ConceptsManagerProps = {
  index: number;
  explanation_type: string;
  onChangeCompleted: () => void;
};
const USER_SELECTED_CONCEPTS = "user_selected_concepts";

export default function ConceptsManager(props: ConceptsManagerProps) {
  const { index, explanation_type, onChangeCompleted } = props;

  const [currentlyUsedConcepts, setCurrentlyUsedConcepts] = useState<string[]>(
    []
  );
  const [availableToBeChosenConcepts, setAvailableToBeChosenConcepts] =
    useState<string[]>([]);

  const [userSelectedConcepts, setUserSelectedConcepts] = useState<string[]>(
    []
  );

  const [isLoading, setLoading] = useState(true);

  useEffect(() => {
    const payload = {
      id: getId(),
      img: index,
      explanation_type,
    };
    http("/explanation-concepts", payload)
      .then((el) => el.json())
      .then((data) => {
        setCurrentlyUsedConcepts(data.usedConcepts);
        setAvailableToBeChosenConcepts(data.availableToBeChosenConcepts);
        setUserSelectedConcepts(data.userSelectedConcepts);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [index, explanation_type]);

  useEffect(() => {
    const payload = {
      id: getId(),
      img: index,
      constraint_type: USER_SELECTED_CONCEPTS,
      concepts: userSelectedConcepts,
    };
    http("/concept-constraint", payload)
      .then((el) => el.json())
      .then(() => {
        onChangeCompleted();
      })
      .catch(() => {});
  }, [userSelectedConcepts]);

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
            onClick={(conceptName) =>
              setUserSelectedConcepts([...userSelectedConcepts, conceptName])
            }
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
            onClick={(conceptName) =>
              setUserSelectedConcepts(
                userSelectedConcepts.filter((el) => el !== conceptName)
              )
            }
          />
        </div>
      </Row>
    </>
  );
}
