import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import DeviceClassForm from 'components/data/manufacturing/deviceClass/form';

export default function UpdateDeviceClass() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <DeviceClassForm 
      id={id} 
      update={true}
    />
  )
}

UpdateDeviceClass.getLayout = getDefaultLayOut;