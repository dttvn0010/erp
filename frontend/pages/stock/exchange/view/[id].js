import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ExchangeForm from 'components/stock/exchange/form';

export default function ViewExchange() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ExchangeForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewExchange.getLayout = getDefaultLayOut;