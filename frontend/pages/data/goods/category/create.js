import { getDefaultLayOut } from 'utils/helper';
import CategoryForm from 'components/data/goods/category/form';

export default function CreateCategory() {
  return(
    <CategoryForm/>
  )
}

CreateCategory.getLayout = getDefaultLayOut;