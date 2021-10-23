import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import CategoryForm from 'components/data/goods/category/form';

export default function UpdateCategory() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <CategoryForm 
      id={id} 
      update={true}
    />
  )
}

UpdateCategory.getLayout = getDefaultLayOut;