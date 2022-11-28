import { Select, Skeleton, Table } from "antd";
import { getId } from "../common/storage";
import { useEffect, useState } from "react";
import { http, httpGet } from "../common/http";
import { CounterfactualExplanation } from "./models/counterfactual_model";
import ConceptsManager from "../concepts/propose_more_consepts";
import toast from "react-hot-toast";

const { Option } = Select;

export default function CounterFactualExplanation({
  index,
}: {
  index: number;
}) {
  const [counterFactualExplanationStep, setCounterFactualExplanationStep] =useState<string>("select");
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
        toast.error(err);
      })
  }, []);

  if (counterFactualLabels.length === 0) {
    return <Skeleton active />;
  }

  const handleConceptSelected = (lable: string) => {
    setCounterFactualClass(lable);
    setCounterFactualExplanationStep("explain");
  };

  return (
    <>
      {counterFactualExplanationStep === "select" && (
        <p>Select counterfactual target class</p>
      )}
      <Select
        defaultValue={counterFactualLabels[0]}
        style={{ width: 200 }}
        onChange={(value) => handleConceptSelected(value)}
      >
        {counterFactualLabels.map((label) => {
          return (
            <Option key={label} value={label}>
              {label}
            </Option>
          );
        })}
      </Select>
      {counterFactualExplanationStep === "explain" && (
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

  const fetchCounterFactualExplanation = () => {
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
  };

  useEffect(() => {
    fetchCounterFactualExplanation();
  }, []);

  if (isLoading) {
    return <Skeleton active />;
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
      <ConceptsManager
        index={imageIndex}
        explanation_type={"counterfactual"}
        onChangeCompleted={() => fetchCounterFactualExplanation()}
      />
      <br />
      <br />

      <p>OriginalClass {counterFactualExplanation.original.class}</p>
      <Table
        columns={renderedOriginalInstanceColumns}
        dataSource={renderedOriginalInstanceValues}
        pagination={false}
      />
      <br />
      <p>Counterfactual: {desiredCounterFactualClass}</p>
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
