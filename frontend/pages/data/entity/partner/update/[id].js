import { useRouter } from 'next/router';
import { getDefaultLayOut } from 'utils/helper';
import PartnerForm from 'components/data/entity/partner/form';

export default function UpdatePartner() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <PartnerForm 
      id={id} 
      update={true}
    />
  )
}

UpdatePartner.getLayout = getDefaultLayOut;