import { getDefaultLayOut } from 'utils/helper';
import CategoryForm from 'components/data/category/form';

export default function CreateCategory() {
  return(
    <CategoryForm/>
  )
}

CreateCategory.getLayout = getDefaultLayOut;