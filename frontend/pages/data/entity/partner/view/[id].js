import { useRouter } from 'next/router';
import { getDefaultLayOut } from 'utils/helper';
import PartnerForm from 'components/data/entity/partner/form';

export default function ViewPartner() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <PartnerForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewPartner.getLayout = getDefaultLayOut;