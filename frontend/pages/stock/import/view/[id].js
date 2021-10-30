import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ImportForm from 'components/stock/import/form';

export default function ViewImport() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ImportForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewImport.getLayout = getDefaultLayOut;