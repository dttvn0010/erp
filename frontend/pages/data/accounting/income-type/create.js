import { getDefaultLayOut } from 'utils/helper';
import IncomeTypeForm from 'components/data/accounting/income-type/form';

export default function CreateIncomeType() {
  
  return(
    <IncomeTypeForm />
  )
}

CreateIncomeType.getLayout = getDefaultLayOut;