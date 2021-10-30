import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ExportForm from 'components/stock/export/form';

export default function ViewExport() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ExportForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewExport.getLayout = getDefaultLayOut;