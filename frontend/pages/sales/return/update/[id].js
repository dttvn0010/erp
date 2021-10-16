import { getDefaultLayOut } from 'utils/helper';
import { useRouter } from 'next/router';
import ReturnForm from 'components/sales/return/form';

export default function UpdateReturn() {
  const router = useRouter()
  const { id } = router.query

  return (
    <ReturnForm 
      id={id}
      update={true}
    />
  )
}

UpdateReturn.getLayout = getDefaultLayOut;