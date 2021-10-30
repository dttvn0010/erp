import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ExportForm from 'components/stock/export/form';

export default function UpdateExport() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ExportForm 
      id={id} 
      update={true}
    />
  )
}

UpdateExport.getLayout = getDefaultLayOut;