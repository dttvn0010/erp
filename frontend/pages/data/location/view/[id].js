import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import LocationForm from 'components/data/location/form';

export default function ViewLocation() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <LocationForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewLocation.getLayout = getDefaultLayOut;