import { Button } from "antd";
import React from "react";

export default function TriggerExplain(props: { index: number }) {
  function handleExplanationRequested() {
    window.location.replace(`/explain/${props.index}`);
  }

  return (
    <Button onClick={handleExplanationRequested} type="primary">
      Explain
    </Button>
  );
}
