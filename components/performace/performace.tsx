import { Col, Row, Statistic } from "antd";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { httpGet } from "../common/http";
import { getId } from "../common/storage";

export default function PerformanceMetrics({
  explanation_type,
}: {
  explanation_type: string;
}) {
  // blackbox metrics
  const [blackBoxAccuracy, setBlackBoxAccuracy] = useState<number>(0);
  // decision tree metrics
  const [desicionTreeAccuracy, setDesicionTreeAccuracy] = useState<number>(0);
  const [desicionTreeFidelity, setDesicionTreeFidelity] = useState<number>(0);
  // counterfactual metrics
  const [counterfactualProbability, setCounterFactualProbability] =
    useState<number>(0);

  const updateMetrics = () => {
    httpGet(`/performance-metrics/${getId()}`)
      .then((el) => el.json())
      .then((data) => {
        const { decisionTree, blackbox, counterfactual } = data;
        setBlackBoxAccuracy(blackbox.accuracy);
        setDesicionTreeAccuracy(decisionTree.accuracy);
        setDesicionTreeFidelity(decisionTree.fidelity);
        setCounterFactualProbability(counterfactual.probability);
      })
      .catch((err) => {
        console.error(err);
        toast.error("Fetching metrics failed");
      });
  };

  useEffect(() => {
    const interval = setInterval(() => updateMetrics(), 5_000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  const showBlackBoxMetrics = explanation_type === "decision_tree";
  const showDecisionTreeMetrics = explanation_type === "decision_tree";
  const showCounterFactualMetrics = explanation_type === "counterfactual";

  return (
    <>
      {showBlackBoxMetrics && (
        <Row>
          <Col span={24}>
            <Statistic
              title="Black box accuracy"
              value={blackBoxAccuracy}
              precision={3}
            />
          </Col>
        </Row>
      )}

      {showDecisionTreeMetrics && (
        <>
          <Row>
            <Col span={24}>
              <Statistic
                title="Decision tree accuracy"
                value={desicionTreeAccuracy}
                precision={3}
              />
            </Col>
          </Row>
          <Row>
            <Col span={24}>
              <Statistic
                title="Decision tree fidelity"
                value={desicionTreeFidelity}
                precision={3}
              />
            </Col>
          </Row>
        </>
      )}

      {showCounterFactualMetrics && (
        <Row>
          <Col span={24}>
            <Statistic
              title="Counterfactual probability"
              value={counterfactualProbability}
              precision={3}
            />
          </Col>
        </Row>
      )}
    </>
  );
}
