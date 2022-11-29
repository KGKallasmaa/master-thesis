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
  // counterfactual metrics
  const [counterfactualProbability, setCounterFactualProbability] =
    useState<number>(0);

  const updateMetrics = () => {
    httpGet(`/performance-metrics/${getId()}`)
      .then((el) => el.json())
      .then((data) => {
        const { decisionTree, blackBox, counterfactual } = data;
        setDesicionTreeAccuracy(decisionTree.accuracy);
        setBlackBoxAccuracy(blackBox.accuracy);
        setCounterFactualProbability(counterfactual.probability);
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
              title="Black box accuraccy"
              value={blackBoxAccuracy}
              precision={3}
            />
          </Col>
        </Row>
      )}

      {showDesisionTreeMetrics && (
        <Row>
          <Col span={24}>
            <Statistic
              title="Desision tree accuraccy"
              value={desicionTreeAccuracy}
              precision={3}
            />
          </Col>
        </Row>
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
