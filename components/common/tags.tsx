import { Tag } from "antd";

type TagProps = {
  color: string;
  values: string[];
  onClick: (value: string) => void;
};

export default function Tags(props: TagProps) {
  const { values, onClick, color } = props;
  if (values.length === 0) {
    return <></>;
  }
  return (
    <>
      {values.map((el) => (
        <div onClick={()=>onClick(el)}>
        <Tag key={el}
            color={color}>
          {el}
        </Tag>
        </div>
      ))}
    </>
  );
}
