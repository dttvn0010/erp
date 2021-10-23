import { useRouter } from 'next/router';
import { getDefaultLayOut } from 'utils/helper';
import ProductForm from 'components/data/goods/product/form';

export default function UpdateProduct() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ProductForm 
      id={id} 
      update={true}
    />
  )
}

UpdateProduct.getLayout = getDefaultLayOut;