import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ExpenseTypeForm from 'components/data/accounting/expenseType/form';

export default function ViewExpenseType() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ExpenseTypeForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewExpenseType.getLayout = getDefaultLayOut;