import { useRouter } from 'next/router';
import { getDefaultLayOut } from "utils/helper";
import { EllipsisDropDown } from 'components/share/ellipsisDropdown';
import Card from 'components/share/card';
import DataTable from 'components/share/datatable';

export default function Inventory() {
  const baseUrl = '/stock/product-quantity';
  const router = useRouter();

  let renders = {
    col3: (_, row, dispatch) => {
      let items = [
        {
          title: 'Xem lịch sử',
          onClick: () => router.push(`./productQuantity/view/${row.pk}`)
        },
      ];
      return (
        <EllipsisDropDown 
          items={items}
        />
      )
    }
  };

  return (
    <Card
    title={`Số lượng hàng khoá trong kho`}
      body={
        <DataTable 
          renders={renders}
          apiUrl={`${baseUrl}/search`}
        />
      }
    />
  )
}

Inventory.getLayout = getDefaultLayOut;