import { Alert } from "antd";
import { useEffect, useState } from "react";
import { httpGet } from "./http";

export default function HealthCheck() {
  const [serverIsHealthy, setServerIsHealthy] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const intervalId = setInterval(() => {
      //assign interval to a variable to clear it.
      setIsLoading(true);
      httpGet("/health")
        .then((el) => el.json())
        .then((data) => {
          setServerIsHealthy(true);
          setIsLoading(false);
        })
        .catch((err) => {
          setServerIsHealthy(false);
          setIsLoading(false);
        });
    }, 10_000);

    return () => clearInterval(intervalId);
  }, []);
  if (serverIsHealthy == true) {
    return null;
  }
  if (isLoading == true) {
    return null;
  }

  return <Alert message="Server is not running" type="error" />;
}
