import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import DepartmentForm from 'components/data/entity/department/form';

export default function UpdateDepartment() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <DepartmentForm 
      id={id} 
      update={true}
    />
  )
}

UpdateDepartment.getLayout = getDefaultLayOut;