import { getDefaultLayOut } from 'utils/helper';
import ExportForm from 'components/stock/export/form';

export default function CreateExport() {
  return(
    <ExportForm/>
  )
}

CreateExport.getLayout = getDefaultLayOut;