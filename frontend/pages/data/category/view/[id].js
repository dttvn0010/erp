import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import CategoryForm from 'components/data/category/form';

export default function ViewCategory() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <CategoryForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewCategory.getLayout = getDefaultLayOut;