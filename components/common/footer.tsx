import { Button } from "antd";
import { useRouter } from "next/router";
import { getId } from "./storage";

export default function Footer() {
  const router = useRouter();
  const handleReset = () => {
    localStorage.clear();
    window.location.href = "http://localhost:3000/";
  };
  const { index } = router.query;
  return (
    <>
      <h3>Explanation Id {getId()}</h3>
      {index ? <h3>ImageId {index}</h3> : ""}
      <br />
      <Button onClick={handleReset} type="danger">
        Reset
      </Button>
    </>
  );
}
