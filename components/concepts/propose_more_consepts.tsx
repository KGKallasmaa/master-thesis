import { Row, Skeleton } from "antd";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { http } from "../common/http";
import { getId } from "../common/storage";
import Tags from "../common/tags";

type ConceptsManagerProps = {
  index: number;
  explanation_type: string;
  onChangeCompleted: () => void;
};
const USER_SELECTED_CONCEPTS = "user_selected_concepts";

function arraysHaveSameElements(a: string[], b: string[]) {
  return a.length === b.length && a.every((v) => b.includes(v));
}

export default function ConceptsManager(props: ConceptsManagerProps) {
  const { index, explanation_type, onChangeCompleted } = props;

  const [isLoading, setLoading] = useState(true);

  const [currentlyUsedConcepts, setCurrentlyUsedConcepts] = useState<string[]>(
    []
  );
  const [availableToBeChosenConcepts, setAvailableToBeChosenConcepts] =
    useState<string[]>([]);

  const [newConceptConstraint, setNewConceptConstraint] = useState<string[]>(
    []
  );

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
        setNewConceptConstraint(data.usedConcepts);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        toast.error(err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [index, explanation_type]);

  useEffect(() => {
    if (arraysHaveSameElements(currentlyUsedConcepts, newConceptConstraint)) {
      return;
    }
    const payload = {
      id: getId(),
      img: index,
      constraint_type: USER_SELECTED_CONCEPTS,
      explanation_type,
      concepts: newConceptConstraint.filter((v, i, a) => a.indexOf(v) === i),
    };
    http("/concept-constraint", payload)
      .then((resp) => {
        if (resp.status === 200 || resp.status === 204) {
          onChangeCompleted();
        }
      })
      .catch(() => {});
  }, [newConceptConstraint]);

  if (isLoading) {
    return <Skeleton active />;
  }

  return (
    <>
      <Row>
        <b>
          {currentlyUsedConcepts.length > 0 ? "Select concepts to remove:" : ""}
        </b>
        <div style={{ marginTop: 15 }}>
          <Tags
            color={"blue"}
            values={currentlyUsedConcepts}
            onClick={(conceptName) =>
              setNewConceptConstraint(
                newConceptConstraint.filter((el) => el !== conceptName)
              )
            }
          />
        </div>
      </Row>
      <Row>
        <b>
          {availableToBeChosenConcepts.length > 0
            ? "Select concepts to add:"
            : ""}
        </b>

        <div style={{ marginTop: 15 }}>
          <Tags
            color={"red"}
            values={availableToBeChosenConcepts}
            onClick={(conceptName) =>
              setNewConceptConstraint([...newConceptConstraint, conceptName])
            }
          />
        </div>
      </Row>
    </>
  );
}
