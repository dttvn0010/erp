import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import DeviceMaintainanceForm from 'components/manufacturing/deviceMaintainance/form';

export default function UpdateDeviceMaintainance() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <DeviceMaintainanceForm 
      id={id} 
      update={true}
    />
  )
}

UpdateDeviceMaintainance.getLayout = getDefaultLayOut;