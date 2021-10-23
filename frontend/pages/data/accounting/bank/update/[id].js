import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import BankForm from 'components/data/accounting/bank/form';

export default function UpdateBank() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <BankForm 
      id={id} 
      update={true}
    />
  )
}

UpdateBank.getLayout = getDefaultLayOut;