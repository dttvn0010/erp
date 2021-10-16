import { useRouter } from 'next/router';
import { getDefaultLayOut } from "utils/helper";

import { EllipsisDropDown } from 'components/share/ellipsis_dropdown';
import Card from "components/share/card";
import DataTable from 'components/share/datatable';
import { 
  IconLink, 
  getStatusSwitcher,
  getDeleteItemHandler
} from 'utils/helper';

const itemName = 'chứng từ mua hàng';

export default function Index() {
  const router = useRouter();
  const baseUrl = '/purchase/voucher/api';
  const deleteItem = getDeleteItemHandler(itemName, `${baseUrl}/crud/[$id$]/`);


  const renders = {
    col3: (data, row, dispatch) => (
      getStatusSwitcher(data, row, dispatch, itemName, `${baseUrl}/change-status/[$id$]`)
    ),

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
            apiUrl={"/purchase/voucher/search"}
          />
        </>
      }
    />
  )
}

Index.getLayout = getDefaultLayOut;