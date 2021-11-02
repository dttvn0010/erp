import { getDefaultLayOut } from 'utils/helper';
import DeviceMaintainanceForm from 'components/manufacturing/deviceMaintainance/form';

export default function CreateDeviceMaintainance() {
  return(
    <DeviceMaintainanceForm />
  )
}

CreateDeviceMaintainance.getLayout = getDefaultLayOut;