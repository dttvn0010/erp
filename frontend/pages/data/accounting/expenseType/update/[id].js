import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ExpenseTypeForm from 'components/data/accounting/expenseType/form';

export default function UpdateExpenseType() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ExpenseTypeForm 
      id={id} 
      update={true}
    />
  )
}

UpdateExpenseType.getLayout = getDefaultLayOut;