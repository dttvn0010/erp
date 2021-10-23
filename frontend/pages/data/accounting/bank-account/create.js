import { getDefaultLayOut } from 'utils/helper';
import BankAccountForm from 'components/data/accounting/bank-account/form';

export default function CreateBankAccount() {
  return(
    <BankAccountForm/>
  )
}

CreateBankAccount.getLayout = getDefaultLayOut;