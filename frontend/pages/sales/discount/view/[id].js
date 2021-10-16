import { getDefaultLayOut } from 'utils/helper';
import { useRouter } from 'next/router';
import DiscountForm from 'components/sales/discount/form';

export default function ViewDiscount() {
  const router = useRouter()
  const { id } = router.query

  return (
    <DiscountForm 
      id={id}
      readOnly={true}
    />
  )
}

ViewDiscount.getLayout = getDefaultLayOut;