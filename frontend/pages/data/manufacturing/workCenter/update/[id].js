import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import WorkCenterForm from 'components/data/manufacturing/workCenter/form';

export default function UpdateWorkCenter() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <WorkCenterForm 
      id={id} 
      update={true}
    />
  )
}

UpdateWorkCenter.getLayout = getDefaultLayOut;