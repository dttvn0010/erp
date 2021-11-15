import { getDefaultLayOut } from 'utils/helper';
import ProductionProcessForm from 'components/manufacturing/productionProcess/form';

export default function CreateProductionProcess() {
  return(
    <ProductionProcessForm />
  )
}

CreateProductionProcess.getLayout = getDefaultLayOut;