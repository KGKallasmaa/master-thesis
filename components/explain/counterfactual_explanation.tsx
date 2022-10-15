import { Select } from "antd";
import { getId } from "../common/storage";
import { useEffect, useState } from "react";
import { http, httpGet } from "../common/http";
const { Option } = Select;

export default function CounterFactualExplanation({
  index,
}: {
  index: number;
}) {
  const [counterFactualClass, setCounterFactualClass] = useState<string>("");
  const [counterFactualLabels, setCouterFactualLabels] = useState<string[]>([]);

  useEffect(() => {
    httpGet("/all-labels")
      .then((el) => el.json())
      .then((data) => {
        setCouterFactualLabels(data.labels);
      })
      .catch((err) => {
        console.error(err);
      })
      .finally(() => {});
  }, []);

  if (counterFactualLabels.length === 0) {
    return <>Loading ...</>;
  }

  return (
    <>
      <Select
        defaultValue={counterFactualLabels[0]}
        style={{ width: 120 }}
        onChange={(value) => setCounterFactualClass(value)}
      >
        {counterFactualLabels.map((label) => {
          return <Option value={label}>{label}</Option>;
        })}
      </Select>

      {counterFactualClass && (
        <Counterfactual
          imageIndex={index}
          desiredCounterFactualClass={counterFactualClass}
        />
      )}
    </>
  );
}
function Counterfactual({
  imageIndex,
  desiredCounterFactualClass,
}: {
  imageIndex: number;
  desiredCounterFactualClass: string;
}) {
  const [counterFactualExplanation, setCounterFactualExplanation] = useState<
    string[]
  >([]);
  const [originalClass, setOriginalClass] = useState<string>("");
  const [isLoading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const payload = {
      img: imageIndex,
      id: getId(),
      counterFactualClass: desiredCounterFactualClass,
    };
    http("/counter-factual-explanation", payload)
      .then((el) => el.json())
      .then((data) => {
        setError(data.error);
        setCounterFactualExplanation(data.counterFactualExplanation);
        setOriginalClass(data.originalClass);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (isLoading) {
    return <p>Loading...</p>;
  }
  if (error || counterFactualExplanation.length === 0) {
    return (
      <>
        <p>Could not generate counterfactuals.</p>
        <p>{error}</p>
      </>
    );
  }

  return (
    <>
      <p>OriginalClass {originalClass}</p>
      <br />
      <p>Counter_factual: {desiredCounterFactualClass}</p>
      <br />
      {counterFactualExplanation.length === 0 && (
        <p>Counterfactual explanation not found</p>
      )}
      {counterFactualExplanation.map((el) => {
        return <p>{el}</p>;
      })}
    </>
  );
}
