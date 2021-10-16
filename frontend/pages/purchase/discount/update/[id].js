import { getDefaultLayOut } from 'utils/helper';
import { useRouter } from 'next/router';
import DiscountForm from 'components/purchase/discount/form';

export default function UpdateDiscount() {
  const router = useRouter()
  const { id } = router.query

  return (
    <DiscountForm 
      id={id}
      update={true}
    />
  )
}

UpdateDiscount.getLayout = getDefaultLayOut;