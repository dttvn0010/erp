import { getDefaultLayOut } from 'utils/helper';
import { useRouter } from 'next/router';
import OrderForm from 'components/purchase/order/form';

export default function ViewOrder() {
  const router = useRouter()
  const { id } = router.query

  return (
    <OrderForm 
      id={id}
      readOnly={true}
    />
  )
}

ViewOrder.getLayout = getDefaultLayOut;