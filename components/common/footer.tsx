import { Button } from "antd";
import { getId } from "./storage";

export default function Footer() {
  const handleReset = () => {
    localStorage.clear();
    window.location.replace("/");
    window.location.reload();
  };
  return (
    <>
      <h2>Explanation Id {getId()}</h2>
      <br />
      <Button onClick={handleReset} type="danger">
        Reset
      </Button>
    </>
  );
}
