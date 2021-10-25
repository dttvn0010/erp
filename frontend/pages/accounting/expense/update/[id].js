import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ExpenseForm from 'components/accounting/expense/form';

export default function UpdateExpense() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ExpenseForm 
      id={id} 
      update={true}
    />
  )
}

UpdateExpense.getLayout = getDefaultLayOut;