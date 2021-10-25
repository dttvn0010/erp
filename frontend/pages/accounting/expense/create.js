import { getDefaultLayOut } from 'utils/helper';
import ExpenseForm from 'components/accounting/expense/form';

export default function CreateExpense() {
  return(
    <ExpenseForm/>
  )
}

CreateExpense.getLayout = getDefaultLayOut;