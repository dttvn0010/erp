import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ProductBomForm from 'components/manufacturing/productBom/form';

export default function UpdateProductBom() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ProductBomForm 
      id={id} 
      update={true}
    />
  )
}

UpdateProductBom.getLayout = getDefaultLayOut;