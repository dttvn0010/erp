import { getDefaultLayOut } from 'utils/helper';
import IncomeForm from 'components/accounting/income/form';

export default function CreateIncome() {
  return(
    <IncomeForm/>
  )
}

CreateIncome.getLayout = getDefaultLayOut;