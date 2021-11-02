import { getDefaultLayOut } from 'utils/helper';
import WorkCenterForm from 'components/data/manufacturing/workCenter/form';

export default function CreateWorkCenter() {
  return(
    <WorkCenterForm />
  )
}

CreateWorkCenter.getLayout = getDefaultLayOut;