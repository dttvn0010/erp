import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import DeviceForm from 'components/data/manufacturing/device/form';

export default function UpdateDevice() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <DeviceForm 
      id={id} 
      update={true}
    />
  )
}

UpdateDevice.getLayout = getDefaultLayOut;