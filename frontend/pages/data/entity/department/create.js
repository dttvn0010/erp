import { getDefaultLayOut } from 'utils/helper';
import DepartmentForm from 'components/data/entity/department/form';

export default function CreateDepartment() {
  return(
    <DepartmentForm/>
  )
}

CreateDepartment.getLayout = getDefaultLayOut;