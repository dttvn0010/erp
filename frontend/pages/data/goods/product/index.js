import { useRouter } from 'next/router';
import { EllipsisDropDown } from 'components/share/ellipsis_dropdown';
import Card from 'components/share/card';
import DataTable from 'components/share/datatable';

import { 
  getDeleteItemHandler, 
  getStatusSwitcher ,
  getDefaultLayOut,
  IconLink
} from 'utils/helper';

const itemName = 'hàng hoá/dịch vụ';

export default function Index() {
  const router = useRouter();
  const baseUrl = '/stock/product/api';
  const deleteItem = getDeleteItemHandler(itemName, `${baseUrl}/crud/[$id$]/`);

  let renders = {
    col2: (data, row, dispatch) => {
      return getStatusSwitcher(data, row, dispatch, itemName, `${baseUrl}/change-status/[$id$]`);
    },

    col3: (_, row, dispatch) => {
      let items = [
        {
          title: 'Xem thông tin',
          onClick: () => router.push(`./product/view/${row.pk}`)
        },
        {
          title: 'Cập nhật',
          onClick: () => router.push(`./product/update/${row.pk}`)
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
  };

  return(
    <Card
      title={`Danh sách ${itemName}`}
      body={
        <>
          <div className="mb-2">
            <IconLink
              href="./product/create"
              icon="plus"
              title={`Thêm ${itemName}`}
            />
          </div>

          <DataTable 
            renders={renders}
            apiUrl={"/stock/product/search"}
          />
        </>
      }
    />
  )
}

Index.getLayout = getDefaultLayOut;