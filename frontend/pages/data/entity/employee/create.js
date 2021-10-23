import { getDefaultLayOut } from 'utils/helper';
import EmployeeForm from 'components/data/entity/employee/form';

export default function CreateEmployee() {
  return(
    <EmployeeForm/>
  )
}

CreateEmployee.getLayout = getDefaultLayOut;