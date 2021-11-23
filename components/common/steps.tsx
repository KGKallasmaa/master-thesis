import {Col, Row, Steps} from 'antd';

const {Step} = Steps;


export enum CurrentStep {
    Upload,
    SelectConcepts
}


export function ExplainableSteps(props: { step: CurrentStep }) {
    return (
        <Row>
            <Col span={2}/>
            <Col span={20}>
                <Steps size="small" current={props.step}>
                    <Step title="Upload image"/>
                    <Step title="Select concepts"/>
                    <Step title="Verify concepts"/>
                </Steps>
            </Col>
            <Col span={2}/>
        </Row>
    )
}