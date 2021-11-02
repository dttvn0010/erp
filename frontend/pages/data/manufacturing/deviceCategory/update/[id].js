import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import DeviceCategoryForm from 'components/data/manufacturing/deviceCategory/form';

export default function UpdateDeviceCategory() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <DeviceCategoryForm 
      id={id} 
      update={true}
    />
  )
}

UpdateDeviceCategory.getLayout = getDefaultLayOut;