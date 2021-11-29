import { useRouter } from 'next/router';
import { getDefaultLayOut } from "utils/helper";

import { EllipsisDropDown } from 'components/share/ellipsisDropdown';
import Card from "components/share/card";
import DataTable from 'components/share/datatable';
import { 
  IconLink, 
  getDeleteItemHandler
} from 'utils/helper';

const itemName = 'chứng từ mua hàng';

export default function Index() {
  const router = useRouter();
  const baseUrl = '/purchase/order';
  const deleteItem = getDeleteItemHandler(itemName, `${baseUrl}/crud/[$id$]/`);


  const renders = {
    col4: (_, row, dispatch) => {
      let items = [
        {
          title: 'Xem thông tin',
          onClick: () => router.push(`./voucher/view/${row.pk}`)
        },
        {
          title: 'Cập nhật',
          onClick: () => router.push(`./voucher/update/${row.pk}`)
        }
      ];

      if(row.status_id === 'DRAFT') {
        items.push({
          title: 'Xóa',
          onClick: () => deleteItem(dispatch, row)
        })
      }

      return (
        <EllipsisDropDown 
          items={items}
        />
      );
    }
  }
  return (
    <Card
      title={`Danh sách ${itemName}`}
      body={
        <>
          <div className="mb-2">
            <IconLink
              href="./voucher/create"
              icon="plus"
              title={`Thêm ${itemName}`}
            />
          </div>

          <DataTable 
            renders={renders}
            apiUrl={`${baseUrl}/search?type=purchase`}
          />
        </>
      }
    />
  )
}

Index.getLayout = getDefaultLayOut;