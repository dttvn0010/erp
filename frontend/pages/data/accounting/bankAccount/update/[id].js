import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import BankAccountForm from 'components/data/accounting/bankAccount/form';

export default function UpdateBankAccount() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <BankAccountForm 
      id={id} 
      update={true}
    />
  )
}

UpdateBankAccount.getLayout = getDefaultLayOut;