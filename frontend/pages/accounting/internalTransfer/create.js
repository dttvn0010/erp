import { getDefaultLayOut } from 'utils/helper';
import InternalTranferForm from 'components/accounting/internalTransfer/form';

export default function CreateInternalTranfer() {
  return(
    <InternalTranferForm />
  )
}

CreateInternalTranfer.getLayout = getDefaultLayOut;