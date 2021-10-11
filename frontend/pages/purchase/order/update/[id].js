import { getDefaultLayOut } from 'utils/helper';
import { useRouter } from 'next/router';
import OrderForm from 'components/purchase/order/form';

export default function UpdateOrder() {
  const router = useRouter()
  const { id } = router.query

  return (
    <OrderForm 
      id={id}
      update={true}
    />
  )
}

UpdateOrder.getLayout = getDefaultLayOut;