import { useRouter } from 'next/router';
import { getDefaultLayOut } from 'utils/helper';
import ProductForm from 'components/data/goods/product/form';

export default function ViewProduct() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ProductForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewProduct.getLayout = getDefaultLayOut;