import { getDefaultLayOut } from 'utils/helper';
import ProductForm from 'components/data/product/form';

export default function CreateProduct() {
  return(
    <ProductForm/>
  )
}

CreateProduct.getLayout = getDefaultLayOut;