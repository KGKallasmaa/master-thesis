import { Select } from "antd";

const { Option } = Select;

interface SelectModelProps {
  models: string[];
  dataSets: string[];

  onModelSelected(newModel: string): void;

  onDataSetSelected(newModel: string): void;
}

export function SelectSection(props: SelectModelProps) {
  const { models, dataSets, onModelSelected, onDataSetSelected } = props;

  return (
    <>
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
