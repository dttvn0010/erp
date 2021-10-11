import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import LocationForm from 'components/data/location/form';

export default function UpdateLocation() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <LocationForm 
      id={id} 
      update={true}
    />
  )
}

UpdateLocation.getLayout = getDefaultLayOut;