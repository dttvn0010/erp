import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import WorkCenterForm from 'components/data/manufacturing/workCenter/form';

export default function ViewWorkCenter() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <WorkCenterForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewWorkCenter.getLayout = getDefaultLayOut;