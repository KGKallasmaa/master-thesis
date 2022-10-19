import { Select, Table } from "antd";
import { getId } from "../common/storage";
import { useEffect, useState } from "react";
import { http, httpGet } from "../common/http";
import { CounterfactualExplanation } from "./models/counterfactual_model";
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
        <>
          <br />
          <br />
          <Counterfactual
            imageIndex={index}
            desiredCounterFactualClass={counterFactualClass}
          />
        </>
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
  const [counterFactualExplanation, setCounterFactualExplanation] =
    useState<CounterfactualExplanation>(null);
  const [isLoading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    const payload = {
      img: imageIndex,
      id: getId(),
      counterFactualClass: desiredCounterFactualClass,
    };

    http("/counter-factual-explanation", payload)
      .then((el) => el.json())
      .then((data) => {
        setCounterFactualExplanation(data);
        setError(data.error);
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
  if (error) {
    return (
      <>
        <p>Could not generate counterfactuals.</p>
        <p>{error}</p>
      </>
    );
  }

  const renderedOriginalInstanceColumns = Object.entries(
    counterFactualExplanation.original.values
  ).map(([feature, _]) => {
    return { title: feature, dataIndex: feature, key: feature };
  });
  const renderedOriginalInstanceValues = [
    counterFactualExplanation.original.values,
  ];

  const counterfactualColumns = Object.entries(
    counterFactualExplanation.counterfactuals[0].values
  ).map(([feature, _]) => {
    return { title: feature, dataIndex: feature, key: feature };
  });

  const renderedCounterfactualValues = Object.entries(
    counterFactualExplanation.counterfactuals
  ).map(([_, counterfactual]) => {
    return counterfactual.values;
  });
  const renderedCounterfactualDif = Object.entries(
    counterFactualExplanation.counterfactuals
  ).map(([_, counterfactual]) => {
    return counterfactual.dif;
  });

  return (
    <>
      <p>OriginalClass {counterFactualExplanation.original.class}</p>
      <Table
        columns={renderedOriginalInstanceColumns}
        dataSource={renderedOriginalInstanceValues}
        pagination={false}
      />
      <br />
      <p>Counter_factual: {desiredCounterFactualClass}</p>
      <br />
      <p>Raw counterfactual values</p>
      <Table
        columns={counterfactualColumns}
        dataSource={renderedCounterfactualValues}
        pagination={false}
      />
      <br />
      <p>Diff counterfactual values</p>
      <Table
        columns={counterfactualColumns}
        dataSource={renderedCounterfactualDif}
        pagination={false}
      />
    </>
  );
}
