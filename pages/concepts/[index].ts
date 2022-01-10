import { useRouter } from "next/router";
import ConceptsTask from "../../components/concepts/concepts_task";

const ConceptMap = () => {
  const router = useRouter();
  const { index } = router.query;
  return ConceptsTask(parseInt(<string>index));
};

export default ConceptMap;
