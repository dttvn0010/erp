import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import EmployeeForm from 'components/data/entity/employee/form';

export default function ViewEmployee() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <EmployeeForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewEmployee.getLayout = getDefaultLayOut;