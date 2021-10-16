import { getDefaultLayOut } from 'utils/helper';
import { useRouter } from 'next/router';
import ReturnForm from 'components/purchase/return/form';

export default function ViewReturn() {
  const router = useRouter()
  const { id } = router.query

  return (
    <ReturnForm 
      id={id}
      readOnly={true}
    />
  )
}

ViewReturn.getLayout = getDefaultLayOut;