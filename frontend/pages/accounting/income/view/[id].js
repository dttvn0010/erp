import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import IncomeForm from 'components/accounting/income/form';

export default function ViewIncome() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <IncomeForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewIncome.getLayout = getDefaultLayOut;