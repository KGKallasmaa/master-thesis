import { ExplainableHeader } from "../common/header";
import { CurrentStep, ExplainableSteps } from "../common/steps";
import { Col, Row, Select } from "antd";
import { getId } from "../common/storage";
import { useEffect, useState } from "react";
import { http, httpGet } from "../common/http";
import { CurrentImage } from "../concepts/current_image";
const { Option } = Select;

// TODO: fetch these labels from the server

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

  if (counterFactualClass === "") {
    return (
      <Select
        defaultValue={counterFactualLabels[0]}
        style={{ width: 120 }}
        onChange={(value) => setCounterFactualClass(value)}
      >
        {counterFactualLabels.map((label) => {
          return <Option value={label}>{label}</Option>;
        })}
      </Select>
    );
  }

  return (
    <Counterfactual
      imageIndex={index}
      desiredCounterFactualClass={counterFactualClass}
    />
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
  if (isLoading) {
    return <p>Loading...</p>;
  }
  if (error !== "") {
    return <p>{error}</p>;
  }
  useEffect(() => {
    const payload = {
      img: imageIndex,
      id: getId(),
      counterFactualClass: desiredCounterFactualClass,
    };
    http("/counterfactual-explanation", payload)
      .then((el) => el.json())
      .then((data) => {
        console.log(data);
        setCounterFactualExplanation(data.counterFactualExplanation);
        setOriginalClass(data.originalClass);
      })
      .catch((err) => {
        console.error(err);
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [imageIndex, desiredCounterFactualClass]);

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
