import { getDefaultLayOut } from 'utils/helper';
import ExchangeForm from 'components/stock/exchange/form';

export default function CreateExchange() {
  return(
    <ExchangeForm/>
  )
}

CreateExchange.getLayout = getDefaultLayOut;