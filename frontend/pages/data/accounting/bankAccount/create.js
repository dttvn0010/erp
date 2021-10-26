import { getDefaultLayOut } from 'utils/helper';
import BankAccountForm from 'components/data/accounting/bankAccount/form';

export default function CreateBankAccount() {
  return(
    <BankAccountForm/>
  )
}

CreateBankAccount.getLayout = getDefaultLayOut;