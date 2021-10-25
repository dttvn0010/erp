import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ExpenseForm from 'components/accounting/expense/form';

export default function ViewExpense() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ExpenseForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewExpense.getLayout = getDefaultLayOut;