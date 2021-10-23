import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import StockForm from 'components/data/goods/stock/form';

export default function ViewStock() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <StockForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewStock.getLayout = getDefaultLayOut;