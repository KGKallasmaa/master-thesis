import {ExplainableHeader} from "../common/header";
import {CurrentStep, ExplainableSteps} from "../common/steps";
import {Col, Row} from "antd";
import {getId} from "../common/storage";
import CurrentImage from "../concepts/current_image";
import {useEffect, useState} from "react";
import {http} from "../common/http";

export default function ExplainTask(index: number) {
    const title = "Explain";
    const description = "Explaining this image using a decision tree";
    return (
        <>
            <br/>
            <ExplainableHeader title={title} description={description}/>
            <br/>
            <ExplainableSteps step={CurrentStep.SelectConcepts}/>
            <br/>
            <Row>
                <Col span={8}/>
                <Col span={8}>
                    <CurrentImage index={index}/>
                    <br/>
                    <MachineLearningExplanation index={index}/>
                </Col>
                <Col span={8}/>
            </Row>
        </>
    );
}

function MachineLearningExplanation(props: { index: number }) {
    const [isLoading, setLoading] = useState(true)
    const [mlExplanations, setExplanations] = useState<string[]>([])
    useEffect(() => {
        const payload = {
            img: props.index,
            id: getId(),
        };
        http("/explain-using-concepts", payload)
            .then((el) => el.json())
            .then((data) => {
                console.log(data)
                setExplanations(data.explanation)
                setLoading(false)
            })
            .catch(() => {
                setLoading(false)
                console.log("Explaining failed")
            });
    }, [props.index]);

    if (isLoading) {
        return (
            <p>loading ...</p>
        )
    }

    return (
        <div>
            {
                mlExplanations.map(el => (
                    <div>
                        <p>{el}</p>
                        <br/>
                    </div>
                ))
            }
        </div>
    )
}
