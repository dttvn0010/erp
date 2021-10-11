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


export default function Index() {
  const router = useRouter();
  const itemName = 'đơn mua hàng';
  const baseUrl = '/purchase/order/api';
  const deleteItem = getDeleteItemHandler(itemName, `${baseUrl}/crud/[$id$]/`);


  const renders = {
    col3: (data, row, dispatch) => (
      getStatusSwitcher(data, row, dispatch, itemName, `${baseUrl}/change-status/[$id$]`)
    ),

    col4: (_, row, dispatch) => {
      let items = [
        {
          title: 'Xem thông tin',
          onClick: () => router.push(`./order/view/${row.pk}`)
        },
        {
          title: 'Cập nhật',
          onClick: () => router.push(`./order/update/${row.pk}`)
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
      title="Danh sách phiếu mua hàng"
      body={
        <>
          <div className="mb-2">
            <IconLink
              href="./order/create"
              icon="plus"
              title="Thêm đơn mua hàng"
            />
          </div>

          <DataTable 
            renders={renders}
            apiUrl={"/purchase/order/search"}
          />
        </>
      }
    />
  )
}

Index.getLayout = getDefaultLayOut;