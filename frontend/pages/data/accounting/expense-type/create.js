import { getDefaultLayOut } from 'utils/helper';
import ExpenseTypeForm from 'components/data/accounting/expense-type/form';

export default function CreateExpenseType() {
  
  return(
    <ExpenseTypeForm />
  )
}

CreateExpenseType.getLayout = getDefaultLayOut;