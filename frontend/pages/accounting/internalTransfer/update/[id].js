import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import InternalTranferForm from 'components/accounting/internalTransfer/form';

export default function UpdateInternalTranfer() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <InternalTranferForm 
      id={id} 
      update={true}
    />
  )
}

UpdateInternalTranfer.getLayout = getDefaultLayOut;