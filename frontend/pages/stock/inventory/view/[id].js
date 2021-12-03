import { useRouter } from 'next/router'
import { getDefaultLayOut } from 'utils/helper';
import InventoryForm from 'components/stock/inventory/form';

export default function ViewInventory() {
  const router = useRouter();
  const { id } = router.query;
  
  return(
    <InventoryForm 
      id={id} 
      readOnly={true}
    />
  )
}

ViewInventory.getLayout = getDefaultLayOut;