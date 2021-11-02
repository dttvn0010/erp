import { getDefaultLayOut } from 'utils/helper';
import DeviceClassForm from 'components/data/manufacturing/deviceClass/form';

export default function CreateDeviceClass() {
  return(
    <DeviceClassForm />
  )
}

CreateDeviceClass.getLayout = getDefaultLayOut;