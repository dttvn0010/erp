import { getDefaultLayOut } from 'utils/helper';
import ImportForm from 'components/stock/import/form';

export default function CreateImport() {
  return(
    <ImportForm/>
  )
}

CreateImport.getLayout = getDefaultLayOut;