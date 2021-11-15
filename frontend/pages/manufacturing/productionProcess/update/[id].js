import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ProductionProcessForm from 'components/manufacturing/productionProcess/form';

export default function UpdateProductionProcess() {
  const router = useRouter();
  const { id } = router.query;

  return(
    <ProductionProcessForm 
      id={id}
      update={true}
    />
  )
}

UpdateProductionProcess.getLayout = getDefaultLayOut;