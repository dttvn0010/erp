import { useRouter } from 'next/router';
import { EllipsisDropDown } from 'components/share/ellipsis_dropdown';
import Card from 'components/share/card';
import DataTable from 'components/share/datatable';

import { 
  getDeleteItemHandler, 
  getStatusSwitcher,
  getDefaultLayOut,
  IconLink
} from 'utils/helper';

export default function Index() {
  const router = useRouter();
  const itemName = 'địa điểm kho';
  const baseUrl = '/stock/location';
  const deleteItem = getDeleteItemHandler(itemName, `${baseUrl}/crud/[$id$]/`);
  
  let renders = {
    col2: (data, row, dispatch) => {
      return getStatusSwitcher(data, row, dispatch, itemName, `${baseUrl}/change-status/[$id$]`)
    },

    col3: (_, row, dispatch) => {
      let items = [
        {
          title: 'Xem thông tin',
          onClick: () => router.push(`./location/view/${row.pk}`)
        },
        {
          title: 'Cập nhật',
          onClick: () => router.push(`./location/update/${row.pk}`)
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
      )
    }
  }

  return (
    <Card
      title="Danh sách địa điểm kho"
      body={
        <>
          <div className="mb-2">
            <IconLink
              href="./location/create"
              icon="plus"
              title="Thêm địa điểm kho"
            />
          </div>
          <DataTable 
            renders={renders}
            apiUrl={`${baseUrl}/search`}
          />
        </>
      }
    />
  )
}

Index.getLayout = getDefaultLayOut;