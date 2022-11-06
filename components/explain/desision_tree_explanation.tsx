import { useEffect, useState } from "react";
import { http } from "../common/http";
import { getId } from "../common/storage";
import CenterConcepts from "../concepts/center_concepts";
import { BidirectionalBar } from '@ant-design/plots';

type FeatureImportance ={
  featureName:string,
  local:number,
  global:number
}

export default function DesisionTreeExplanation(props: { index: number }) {
  const [isLoading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState(null);
  const [conceptsHaveBeenSelected, setConceptsHaveBeenSelected] =
    useState(false);
  const [featureImportance,setFeatureImportance] = useState<FeatureImportance[]>([]);
  const [trueLabel, setTrueLabel] = useState<string>("");
  const [predictedLabel, setPredictedLabel] = useState<string>("");

  useEffect(() => {
    const { index } = props;
    if (!conceptsHaveBeenSelected) {
      return;
    }
    if (!index) {
      setErrorMessage("Image index not found");
      return;
    }
    const payload = {
      img: index,
      id: getId(),
    };
    http("/decision-tree-explanation", payload)
      .then((el) => el.json())
      .then((data) => {
        setTrueLabel(data.trueLabel);
        setPredictedLabel(data.predictedLabel);
        setFeatureImportance(data.featureImportance);
      })
      .catch((err) => {
        setErrorMessage(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [props.index, conceptsHaveBeenSelected]);

  if (conceptsHaveBeenSelected === false) {
    return (
      <CenterConcepts
        index={props.index}
        explanation_type={"decision_tree"}
        onComplete={() => setConceptsHaveBeenSelected(true)}
      />
    );
  }

  if (isLoading) {
    return <>Generating an explanation ...</>;
  }
  if (errorMessage && !featureImportance) {
    return (
      <div>
        <h3>Explanation has failed</h3>
        <p>{errorMessage}</p>
      </div>
    );
  }

  return (
    <div>
      <h3>{trueLabel}</h3>
      <br />
      <h3>{predictedLabel}</h3>

      <br />
      <h3>Feature importance</h3>
      <br />
      <p>Global - how imortant a feature is the desision tree (%)</p>
      <p>Local - how imortant a feature is explaining this instance (%)</p>
      <br />
      <DesisionTreeGraph data={ featureImportance}/>
    </div>
  );
}


function DesisionTreeGraph(props: { data: FeatureImportance[]; }){
    let{data} = props
    data = data.map()
    const config = {
      data,
      xField: 'featureName',
      xAxis: {
        position: 'bottom',
      },
      interactions: [
        {
          type: 'active-region',
        },
      ],
      yField: ['local', 'global'],
      tooltip: {
        shared: true,
        showMarkers: false,
      },
    };
    return <BidirectionalBar {...config} />;
}