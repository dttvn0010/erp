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
  const itemName = 'ngân hàng';
  const baseUrl = '/accounting/bank';
  const deleteItem = getDeleteItemHandler(itemName, `${baseUrl}/crud/[$id$]/`);
  
  let renders = {
    col0: (data) => {
      if(data) {
        return (<img style={{maxWidth:'100%', maxHeight: "100px"}} src={data}/>)
      }
    },
    col3: (data, row, dispatch) => {
      return getStatusSwitcher(data, row, dispatch, itemName, `${baseUrl}/change-status/[$id$]`)
    },

    col4: (_, row, dispatch) => {
      let items = [
        {
          title: 'Xem thông tin',
          onClick: () => router.push(`./bank/view/${row.pk}`)
        },
        {
          title: 'Cập nhật',
          onClick: () => router.push(`./bank/update/${row.pk}`)
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
              href="./bank/create"
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