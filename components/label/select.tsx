import { Select } from "antd";
import {useEffect, useState} from "react";
import {http} from "../common/http";

const { Option } = Select;

interface SelectModelProps {
  models: string[];
  dataSets: string[];

  onModelSelected(newModel: string): void;
  onLabelSelected(newLabel:string):void;
  onDataSetSelected(newModel: string): void;
}

export function SelectSection(props: SelectModelProps) {
  const { models, dataSets, onModelSelected, onDataSetSelected,onLabelSelected } = props;

  const [labels,setLabels] = useState([])

    useEffect(() => {
        http("/all-labels",{})
            .then((el) => el.json())
            .then((data) => {
                setLabels(data.labels)
            });
    },[]);


  return (
    <>
        {
            labels && (
                <>
                    <Select
                        defaultValue={labels[0]}
                        onChange={(value) => onLabelSelected(value)}
                    >
                        {labels.map((label) => (
                            <Option key={label} value={label}>
                                {label}
                            </Option>
                        ))}
                    </Select>
                    <br />
                    <br />
                </>
            )
        }
      <Select
        defaultValue={models[0]}
        onChange={(value) => onModelSelected(value)}
      >
        {models.map((model) => (
          <Option key={model} value={model}>
            {model}
          </Option>
        ))}
      </Select>
      <br />
      <br />
      <Select
        defaultValue={dataSets[0]}
        onChange={(value) => onDataSetSelected(value)}
      >
        {dataSets.map((data) => (
          <Option key={data} value={data}>
            {data}
          </Option>
        ))}
      </Select>
    </>
  );
}
