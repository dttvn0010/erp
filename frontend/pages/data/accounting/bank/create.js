import { getDefaultLayOut } from 'utils/helper';
import BankForm from 'components/data/accounting/bank/form';

export default function CreateBank() {
  return(
    <BankForm/>
  )
}

CreateBank.getLayout = getDefaultLayOut;