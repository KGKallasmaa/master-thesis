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
  // desision tree metrics
  const [desicionTreeAccuracy, setDesicionTreeAccuracy] = useState<number>(0);
  const [desicionTreeFidelity, setDesicionTreeFidelity] = useState<number>(0);
  // counterfactual metrics
  const [counterfactualProbability, setCounterFactualProbability] =
    useState<number>(0);
  const [counterfactualFidelity, setCounterFactualFidelity] =
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
        setCounterFactualFidelity(counterfactual.fidelity)
      })
      .catch((err) => {
        console.error(err);
        toast.error(err);
      });
  };

  useEffect(() => {
    const interval = setInterval(() => updateMetrics(), 5 * 1000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  const showBlackBoxMetrics = explanation_type === "desision_tree";
  const showDesisionTreeMetrics = explanation_type === "desision_tree";
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

      {showDesisionTreeMetrics && (
        <>
          <Row>
            <Col span={24}>
              <Statistic
                title="Desision tree accuracy"
                value={desicionTreeAccuracy}
                precision={3}
              />
            </Col>
          </Row>
          <Row>
            <Col span={24}>
              <Statistic
                title="Desision tree fidelity"
                value={desicionTreeFidelity}
                precision={3}
              />
            </Col>
          </Row>
        </>
      )}

      {showCounterFactualMetrics && (
        <>
        <Row>
          <Col span={24}>
            <Statistic
              title="Counterfactual probability"
              value={counterfactualProbability}
              precision={3}
            />
          </Col>
        </Row>
        <Row>
            <Col span={24}>
              <Statistic
                title="Counterfactual fidelity"
                value={counterfactualFidelity}
                precision={3}
              />
            </Col>
          </Row>
        </ > 
      )}
    </>
  );
}
