import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import DeviceCategoryForm from 'components/data/manufacturing/deviceCategory/form';

export default function ViewDeviceCategory() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <DeviceCategoryForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewDeviceCategory.getLayout = getDefaultLayOut;