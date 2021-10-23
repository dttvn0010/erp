import { getDefaultLayOut } from 'utils/helper';
import PartnerForm from 'components/data/entity/partner/form';

export default function CreatePartner() {
  return(
    <PartnerForm/>
  )
}

CreatePartner.getLayout = getDefaultLayOut;