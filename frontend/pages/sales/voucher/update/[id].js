import { getDefaultLayOut } from 'utils/helper';
import { useRouter } from 'next/router';
import VoucherForm from 'components/sales/voucher/form';

export default function UpdateVoucher() {
  const router = useRouter()
  const { id } = router.query

  return (
    <VoucherForm 
      id={id}
      update={true}
    />
  )
}

UpdateVoucher.getLayout = getDefaultLayOut;