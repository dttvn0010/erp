import { useRouter } from 'next/router';
import { getDefaultLayOut } from "utils/helper";

import { EllipsisDropDown } from 'components/share/ellipsisDropdown';
import Card from "components/share/card";
import DataTable from 'components/share/datatable';
import { 
  IconLink, 
  getStatusSwitcher,
  getDeleteItemHandler
} from 'utils/helper';

const itemName = 'chứng từ giảm giá hàng bán';

export default function Index() {
  const router = useRouter();
  const baseUrl = '/sales/discount/api';
  const deleteItem = getDeleteItemHandler(itemName, `${baseUrl}/crud/[$id$]/`);


  const renders = {
    col3: (data, row, dispatch) => (
      getStatusSwitcher(data, row, dispatch, itemName, `${baseUrl}/change-status/[$id$]`)
    ),

    col4: (_, row, dispatch) => {
      let items = [
        {
          title: 'Xem thông tin',
          onClick: () => router.push(`./discount/view/${row.pk}`)
        },
        {
          title: 'Cập nhật',
          onClick: () => router.push(`./discount/update/${row.pk}`)
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
              href="./discount/create"
              icon="plus"
              title={`Thêm ${itemName}`}
            />
          </div>

          <DataTable 
            renders={renders}
            apiUrl={"/sales/discount/search"}
          />
        </>
      }
    />
  )
}

Index.getLayout = getDefaultLayOut;