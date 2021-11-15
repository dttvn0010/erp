import { getDefaultLayOut } from 'utils/helper';
import ProductionWorkflowForm from 'components/manufacturing/productionWorkflow/form';

export default function CreateProductionWorkflow() {
  return(
    <ProductionWorkflowForm />
  )
}

CreateProductionWorkflow.getLayout = getDefaultLayOut;