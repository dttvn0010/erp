import { getDefaultLayOut } from 'utils/helper';
import InventoryForm from 'components/stock/inventory/form';

export default function CreateInventory() {
  return(
    <InventoryForm/>
  )
}

CreateInventory.getLayout = getDefaultLayOut;