import { getDefaultLayOut } from 'utils/helper';
import InternalTranferForm from 'components/accounting/internal-transfer/form';

export default function CreateInternalTranfer() {
  return(
    <InternalTranferForm />
  )
}

CreateInternalTranfer.getLayout = getDefaultLayOut;