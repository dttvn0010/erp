import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ProductionWorkflowForm from 'components/manufacturing/productionWorkflow/form';

export default function ViewProductionWorkflow() {
  const router = useRouter();
  const { id } = router.query;

  return(
    <ProductionWorkflowForm 
      id={id}
      readOnly={true}
    />
  )
}

ViewProductionWorkflow.getLayout = getDefaultLayOut;