import { Row, Col } from "antd";
import { useState } from "react";
import { SelectSection } from "./select";
import { CorrectLabelingTask } from "./correct_lable";

export default function Label() {
  // TODO: get real data
  const allModels = ["model-1", "model-2", "model-3"];
  const allDataSets = ["dataset-1", "dataset-2", "dataset-3"];

  const [currentLabel, setLabel] = useState("");

  const [model, setModel] = useState(allModels[0]);
  const [dataSet, setDataSet] = useState(allDataSets[0]);

  return (
    <>
      <br />
      <Row>
        <Col span={1} />
        <Col span={7}>
          <SelectSection
            models={allModels}
            dataSets={allDataSets}
            onModelSelected={setModel}
            onDataSetSelected={setDataSet}
            onLabelSelected={setLabel}
          />
        </Col>
        <Col span={16}>
          <CorrectLabelingTask
            model={model}
            dataset={dataSet}
            label={currentLabel}
          />
        </Col>
      </Row>
    </>
  );
}
