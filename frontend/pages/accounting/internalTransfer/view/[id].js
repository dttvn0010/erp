import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import InternalTranferForm from 'components/accounting/internalTransfer/form';

export default function ViewInternalTranfer() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <InternalTranferForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewInternalTranfer.getLayout = getDefaultLayOut;