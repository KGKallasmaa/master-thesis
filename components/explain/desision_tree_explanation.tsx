import { useEffect, useState } from "react";
import { http } from "../common/http";
import { getId } from "../common/storage";
import { BidirectionalBar } from "@ant-design/plots";
import ConceptsManager from "../concepts/propose_more_consepts";
import { Skeleton } from "antd";

type FeatureImportance = {
  featureName: string;
  local: number;
  global: number;
};

export default function DesisionTreeExplanation(props: { index: number }) {
  const [isLoading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState(null);

  const [featureImportance, setFeatureImportance] = useState<
    FeatureImportance[]
  >([]);
  const { index } = props;
  const [trueLabel, setTrueLabel] = useState<string>("");
  const [predictedLabel, setPredictedLabel] = useState<string>("");

  const fetchDesisionTreeExplanation = () => {
    setLoading(true);
    const payload = {
      img: index,
      id: getId(),
    };
    http("/decision-tree-explanation", payload)
      .then((el) => el.json())
      .then((data) => {
        setTrueLabel(data.trueLabel);
        setPredictedLabel(data.predictedLabel);
        setFeatureImportance(data.featureImportance);
      })
      .catch((err) => {
        setErrorMessage(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchDesisionTreeExplanation();
  }, [index]);

  if (isLoading) {
    return <Skeleton active />;
  }
  if (errorMessage && !featureImportance) {
    return (
      <div>
        <h3>Explanation has failed</h3>
        <p>{errorMessage}</p>
      </div>
    );
  }

  return (
    <div>
      <h3>{trueLabel}</h3>
      <br />
      <h3>{predictedLabel}</h3>
      <br />
      <h3>Feature importance</h3>
      <br />
      <p>Global - how imortant a feature is the desision tree (%)</p>
      <p>Local - how imortant a feature is explaining this instance (%)</p>
      <br />
      <ConceptsManager
        index={index}
        explanation_type={"decision_tree"}
        onChangeCompleted={() => fetchDesisionTreeExplanation()}
      />
      <br />
      <DesisionTreeGraph data={featureImportance} />
    </div>
  );
}

function DesisionTreeGraph(props: { data: FeatureImportance[] }) {
  const { data } = props;
  const config = {
    data,
    xField: "featureName",
    xAxis: {
      position: "bottom",
    },
    interactions: [
      {
        type: "active-region",
      },
    ],
    yField: ["local", "global"],
    tooltip: {
      shared: true,
      showMarkers: false,
    },
  };
  // @ts-ignore
  return <BidirectionalBar {...config} />;
}
