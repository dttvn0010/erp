import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import BankAccountForm from 'components/data/accounting/bankAccount/form';

export default function ViewBankAccount() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <BankAccountForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewBankAccount.getLayout = getDefaultLayOut;