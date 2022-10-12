export default function MachineLearningExplanation(props: { index: number }) {
  const [isLoading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState(null);

  const [explanations, setExplanations] = useState<string[]>([]);
  const [plainTreeExplanation, setPlainTreeExplanation] = useState<string[]>(
    []
  );
  const [trueLabel, setTrueLabel] = useState<string>("");
  const [predictedLabel, setPredictedLabel] = useState<string>("");

  useEffect(() => {
    const { index } = props;
    if (!index) {
      setErrorMessage("Image index not found");
      return;
    }
    const payload = {
      img: index,
      id: getId(),
    };
    http("/explain-using-concepts", payload)
      .then((el) => el.json())
      .then((data) => {
        setTrueLabel(data.trueLabel);
        setPredictedLabel(data.predictedLabel);
        setExplanations(data.explanations);
        setPlainTreeExplanation(data.plainTextTree);
      })
      .catch((err) => {
        setErrorMessage(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [props.index]);

  if (isLoading) {
    return <p>generating an explanation ...</p>;
  }
  if (errorMessage && !explanations) {
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
      <h3>Path explanations</h3>
      <br />
      {explanations.map((el) => (
        <div>
          <p>{el}</p>
          <br />
        </div>
      ))}
      <h3>Tree representation</h3>
      <br />
      {plainTreeExplanation.map((el) => (
        <div>
          <p>
            {extraSpace(el)}
            {el}
          </p>
          <br />
        </div>
      ))}
    </div>
  );
}
function extraSpace(row) {
  const extraSpace = Array(3).fill("\xa0").join("");
  const indexLevelSymbol = "|";
  const nrOfAccourances = row.split(indexLevelSymbol).length - 1; //4

  let space = "";
  for (let i = 0; i < nrOfAccourances - 1; i++) {
    space += extraSpace;
  }
  return space;
}
