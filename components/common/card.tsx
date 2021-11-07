import {Card} from "antd";
import {CloseCircleOutlined, CheckCircleOutlined} from '@ant-design/icons';


const {Meta} = Card;

interface ConceptCardProps {
    label?: string,
    imageUrl: string,
    imageWidth: number,

    onSelected(name: string, isRelevant: boolean): void,
}

export function ConceptCard(props: ConceptCardProps) {
    const {label, imageUrl, onSelected, imageWidth} = props;
    return (
        <>
            <Card
                style={{width: 300}}
                cover={
                    <img
                        alt="to-be-labeled-image"
                        src={imageUrl}
                        width={imageWidth}
                        height={imageWidth}
                    />
                }
                actions={[
                    <CheckCircleOutlined key="yes" onClick={() => onSelected(label, true)}/>,
                    <CloseCircleOutlined key="no" onClick={() => onSelected(label, false)}/>,
                ]}
            >
                <Meta
                    title={label}
                />
            </Card>
        </>
    )
}