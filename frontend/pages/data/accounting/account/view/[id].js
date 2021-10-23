import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';

export default function ViewAccount() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <>Xem tài khoản kế toán : {id}</>
  )
}

ViewAccount.getLayout = getDefaultLayOut;