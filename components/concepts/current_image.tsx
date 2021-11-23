import { Skeleton } from "antd";
import { useEffect, useState } from "react";
import { ConceptCard } from "../common/card";
import { http } from "../common/http";

export default function CurrentImage(props: { index: number }) {
  const { index } = props;
  const [image, setImage] = useState("");
  const [label, setLabel] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const payload = {
      index: index,
    };
    http("/image-by-index", payload)
      .then((el) => el.json())
      .then((data) => {
        setImage(data.url);
        setLabel(data.label);
        setIsLoading(false);
      })
      .catch(() => {
        setIsLoading(false);
      });
  }, [index]);

  if (isLoading) {
    return <Skeleton active />;
  }

  return (
    <ConceptCard
      label={label}
      imageBase64={image}
      imageWidth={200}
      onSelected={null}
    />
  );
}
