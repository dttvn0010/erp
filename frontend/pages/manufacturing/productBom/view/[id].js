import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import ProductBomForm from 'components/manufacturing/productBom/form';

export default function ViewProductBom() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <ProductBomForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewProductBom.getLayout = getDefaultLayOut;