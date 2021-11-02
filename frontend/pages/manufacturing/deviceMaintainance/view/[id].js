import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import DeviceMaintainanceForm from 'components/manufacturing/deviceMaintainance/form';

export default function ViewDeviceMaintainance() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <DeviceMaintainanceForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewDeviceMaintainance.getLayout = getDefaultLayOut;