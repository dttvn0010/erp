import { getDefaultLayOut } from 'utils/helper';
import LocationForm from 'components/data/location/form';

export default function CreateLocation() {
  return(
    <LocationForm/>
  )
}

CreateLocation.getLayout = getDefaultLayOut;