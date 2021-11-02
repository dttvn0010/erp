import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import DeviceClassForm from 'components/data/manufacturing/deviceClass/form';

export default function ViewDeviceClass() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <DeviceClassForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewDeviceClass.getLayout = getDefaultLayOut;