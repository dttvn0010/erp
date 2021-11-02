import { getDefaultLayOut } from 'utils/helper';
import DeviceForm from 'components/data/manufacturing/device/form';

export default function CreateDevice() {
  return(
    <DeviceForm />
  )
}

CreateDevice.getLayout = getDefaultLayOut;