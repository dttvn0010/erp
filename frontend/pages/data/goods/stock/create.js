import { getDefaultLayOut } from 'utils/helper';
import StockForm from 'components/data/goods/stock/form';

export default function CreateStock() {
  return(
    <StockForm/>
  )
}

CreateStock.getLayout = getDefaultLayOut;