import { Row, Col } from "antd";
import { ConceptCard } from "../common/card";

interface CorrectLabelingTaskProps {
  model: string;
  dataset: string;
}

export function CorrectLabelingTask(props: CorrectLabelingTaskProps) {
  function handleCategoryIsRelevant(name: string, decision: boolean) {}

  function handleConceptIsRelevant(name: string, decision: boolean) {}

  // TODO: fetch real data
  const imageUrl =
    "https://media.architecturaldigest.com/photos/5eac5fa22105f13b72dede45/master/pass/111LexowAve_Aug18-1074.jpg";
  const label = "Bed room";
  const conceptsFromImage = [
    {
      conceptName: "Bed",
      src: "https://www.godrejinterio.com/imagestore/B2C/56101515SD00434/56101515SD00434_01_803x602.png",
    },
    {
      conceptName: "Lamp",
      src: "https://cdn.ambientedirect.com/chameleon/mediapool/thumbs/e/14/Artemide_Choose-Tavolo-Tischleuchte_1200x630-ID1244137-6b26b748c53db9143ef4cc7a64deb941.jpg",
    },
    {
      conceptName: "Window",
      src: "https://lda.lowes.com/is/image/Lowes/DP18-161346_NPC_HT_MeasureWindows_AH?scl=1",
    },
    {
      conceptName: "Mirror",
      src: "https://m.media-amazon.com/images/I/51B0uz2znGL._AC_SX466_.jpg",
    },
  ];

  const { model, dataset } = props;
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

      <br />

      <h3>Select relevant concepts</h3>
      <p>
        Please select concepts that can be associated with label <b>{label}</b>
      </p>
      <br />
      <Row>
        {conceptsFromImage.map((el) => (
          <Col
            key={el.conceptName}
            span={8}
            style={{ marginRight: 50, marginBottom: 20 }}
          >
            <ConceptCard
              label={el.conceptName}
              imageUrl={el.src}
              imageWidth={200}
              onSelected={handleConceptIsRelevant}
            />
          </Col>
        ))}
      </Row>
    </>
  );
}
