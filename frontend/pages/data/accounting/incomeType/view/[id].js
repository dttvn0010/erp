import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import IncomeTypeForm from 'components/data/accounting/incomeType/form';

export default function ViewIncomeType() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <IncomeTypeForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewIncomeType.getLayout = getDefaultLayOut;