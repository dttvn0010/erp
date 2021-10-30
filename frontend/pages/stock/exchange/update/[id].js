import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ExchangeForm from 'components/stock/exchange/form';

export default function UpdateExchange() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ExchangeForm 
      id={id} 
      update={true}
    />
  )
}

UpdateExchange.getLayout = getDefaultLayOut;