import { useRouter } from "next/router";
import ExplainTask from "../../components/steps/explain_task";

export default function ExplainPage() {
  const router = useRouter();
  const { index } = router.query;
  // @ts-ignore
  if (!parseInt(index)){
    return null;
  }
  return ExplainTask(parseInt(index));
}
