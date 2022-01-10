import {useRouter} from "next/router";
import ExplainTask from "../../components/explain/explain_task";

const ExplainMap = () => {
  const router = useRouter();
  const {index} = router.query;
  return ExplainTask(parseInt(<string>index));
};

export default ExplainMap;
