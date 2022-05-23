import { Card } from "antd";
import { CloseCircleOutlined, CheckCircleOutlined } from "@ant-design/icons";

const { Meta } = Card;

interface ConceptCardProps {
  label?: string;
  imageBase64: string;
  imageWidth: number;
  onSelected?(name: string, isRelevant: boolean): void;
  title: string;
}

export function ConceptCard(props: ConceptCardProps) {
  const { label, imageBase64, onSelected, imageWidth, title } = props;
  const imageUrl = `data:image/jpeg;base64,${imageBase64}`;
  if (onSelected == null) {
    return (
      <Card
        style={{ width: 300 }}
        title={title}
        cover={
          <img
            alt="to-be-labeled-image"
            src={imageUrl}
            width={imageWidth}
            height={imageWidth}
          />
        }
      >
        <Meta title={label} />
      </Card>
    );
  }
  return (
    <Card
      style={{ width: 300 }}
      cover={
        <img
          alt="to-be-labeled-image"
          src={imageUrl}
          width={imageWidth}
          height={imageWidth}
        />
      }
      actions={[
        <CheckCircleOutlined
          key="yes"
          onClick={() => onSelected(label, true)}
        />,
        <CloseCircleOutlined
          key="no"
          onClick={() => onSelected(label, false)}
        />,
      ]}
    >
      <Meta title={label} />
    </Card>
  );
}
