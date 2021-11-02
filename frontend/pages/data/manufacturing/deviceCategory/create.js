import { getDefaultLayOut } from 'utils/helper';
import DeviceCategoryForm from 'components/data/manufacturing/deviceCategory/form';

export default function CreateDeviceCategory() {
  return(
    <DeviceCategoryForm />
  )
}

CreateDeviceCategory.getLayout = getDefaultLayOut;