import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import IncomeForm from 'components/accounting/income/form';

export default function UpdateIncome() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <IncomeForm 
      id={id} 
      update={true}
    />
  )
}

UpdateIncome.getLayout = getDefaultLayOut;