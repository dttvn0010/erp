import { useRouter } from 'next/router';
import { EllipsisDropDown } from 'components/share/ellipsisDropdown';
import Card from 'components/share/card';
import DataTable from 'components/share/datatable';

import { 
  getDeleteItemHandler, 
  getDefaultLayOut,
  IconLink
} from 'utils/helper';

const itemName = 'lịch bảo trì thiết bị';

export default function Index() {
  const router = useRouter();
  const baseUrl = '/mfr/device-maintainance';
  const deleteItem = getDeleteItemHandler(itemName, `${baseUrl}/crud/[$id$]/`);
  
  let renders = {

    col4: (_, row, dispatch) => {
      let items = [
        {
          title: 'Xem thông tin',
          onClick: () => router.push(`./deviceMaintainance/view/${row.pk}`)
        },
        {
          title: 'Cập nhật',
          onClick: () => router.push(`./deviceMaintainance/update/${row.pk}`)
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
      title={`Danh sách ${itemName}`}
      body={
        <>
          <div className="mb-2">
            <IconLink
              href="./deviceMaintainance/create"
              icon="plus"
              title={`Thêm ${itemName}`}
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