import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import DepartmentForm from 'components/data/entity/department/form';

export default function ViewDepartment() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <DepartmentForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewDepartment.getLayout = getDefaultLayOut;