import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import EmployeeForm from 'components/data/entity/employee/form';

export default function UpdateEmployee() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <EmployeeForm 
      id={id} 
      update={true}
    />
  )
}

UpdateEmployee.getLayout = getDefaultLayOut;