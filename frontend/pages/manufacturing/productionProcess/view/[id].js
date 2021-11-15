import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ProductionProcessForm from 'components/manufacturing/productionProcess/form';

export default function ViewProductionProcess() {
  const router = useRouter();
  const { id } = router.query;

  return(
    <ProductionProcessForm 
      id={id}
      readOnly={true}
    />
  )
}

ViewProductionProcess.getLayout = getDefaultLayOut;