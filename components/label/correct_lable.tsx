import {Row, Col} from 'antd';
import {ConceptCard} from "../common/card";
import {useEffect, useState} from "react";
import {http} from "../common/http";

interface CorrectLabelingTaskProps {
    model: string,
    dataset: string,
}

export function CorrectLabelingTask(props: CorrectLabelingTaskProps) {

    function handleCategoryIsRelevant(name: string, decision: boolean) {
    }

    function handleConceptIsRelevant(name: string, decision: boolean) {
    }

    const [imageUrl, setImageUrl] = useState("");
    const [conceptsFromImage, setConceptsFromImage] = useState([])
    const label = "Bed room"

    useEffect(() => {
        const payload = {
            "label": label
        }
        http("/label-image", payload)
            .then(resp => resp.json())
            .then(data => {
                setImageUrl(data.url)
            })

        http("/label-concepts", payload)
            .then(resp => resp.json())
            .then(data => {
                setConceptsFromImage(data.results)
            })
    })


    const {model, dataset} = props
    return (
        <>

            <h3>Label image association</h3>
            <p>Can this image be associated with this concept</p>
            <Row>
                <ConceptCard
                    key={label}
                    label={label}
                    imageUrl={imageUrl}
                    imageWidth={300}
                    onSelected={handleCategoryIsRelevant}
                />
            </Row>

            <br/>

            <h3>Select relevant concepts</h3>
            <p>Please select concepts that can be associated with label <b>{label}</b></p>
            <br/>
            <Row>
                {
                    conceptsFromImage?.map(el => (
                        <Col key={el.conceptName} span={8} style={{marginRight: 50, marginBottom: 20}}>
                            <ConceptCard
                                label={el.conceptName}
                                imageUrl={el.src}
                                imageWidth={200}
                                onSelected={handleConceptIsRelevant}
                            />
                        </Col>
                    ))
                }
            </Row>
        </>
    )
}

