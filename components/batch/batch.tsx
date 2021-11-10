import { useState } from "react";
import { Col, Row } from "antd";
import { SelectSection } from "../label/select";
import { BatchSelect } from "./batch_select";

export default function Batch() {
  // TODO: get real data
  const allModels = ["model-1", "model-2", "model-3"];
  const allDataSets = ["dataset-1", "dataset-2", "dataset-3"];

  const [model, setModel] = useState(allModels[0]);
  const [dataSet, setDataSet] = useState(allDataSets[0]);

  const [currentLabel,setLabel] = useState("");

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
          <BatchSelect label={currentLabel} model={model} dataset={dataSet} />
        </Col>
      </Row>
    </>
  );
}
