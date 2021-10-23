import { useRouter } from 'next/router';
import { EllipsisDropDown } from 'components/share/ellipsis_dropdown';
import Card from 'components/share/card';
import DataTable from 'components/share/datatable';

import { 
  getDefaultLayOut,
  IconLink
} from 'utils/helper';

export default function Index() {
  const router = useRouter();
  const itemName = 'tài khoản kế toán';
  const baseUrl = '/accounting/account';
  
  let renders = {
    col4: (_, row, dispatch) => {
      let items = [
        {
          title: 'Xem thông tin',
          onClick: () => router.push(`./department/view/${row.pk}`)
        },
      ];

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