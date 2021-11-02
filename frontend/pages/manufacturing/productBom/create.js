import { getDefaultLayOut } from 'utils/helper';
import ProductBomForm from 'components/manufacturing/productBom/form';

export default function CreateProductBom() {
  return(
    <ProductBomForm />
  )
}

CreateProductBom.getLayout = getDefaultLayOut;