import { useRouter } from "next/router";
import ExplainTask from "../../../components/explain/explain_task";

const ExplainMap = () => {
  const router = useRouter();
  const { index, explanation_type } = router.query;
  return ExplainTask(parseInt(<string>index), explanation_type);
};

export default ExplainMap;
