import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';

const itemName = 'nhân viên';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'department',
      label: 'Phòng/ban làm việc',
      type: 'async-select',
      attrs: {
        optionsUrl: '/employee/search-department',
        labelField: 'name'
      }
    },

    {
      name: 'code',
      label: 'Mã nhân viên',
      type: 'input'
    },

    {
      name: 'name',
      label: 'Tên',
      type: 'input'
    },

    {
      name: 'email',
      label: 'Email',
      type: 'input'
    },

    {
      name: 'phone',
      label: 'Số điện thoại',
      type: 'input'
    },
  ],
  detailUrl: '/employee/crud/[$id$]',
  createUrl: '/employee/crud/',
  updateUrl: '/employee/crud/[$id$]/'
};

export default function StockForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../employee';
  const editUrl = id? `../update/${id}` : null;
  const router = useRouter();

  useEffect(() => {
    setForm(createForm(formMeta, update, id, readOnly));
  }, [id]);

  if(!form) return <></>;

  const title = (
    readOnly? `Xem ${itemName}` : (update? `Cập nhập ${itemName}` : `Tạo mới ${itemName}`)
  );

  return(
    <Card
      title={title}
      body={
        <div className="row">
          <div className="col-9">
            <form.All 
              headerWidth={"30%"}
              onSaveSuccess={() => router.push(backUrl)}
              backUrl={backUrl}
              editUrl={editUrl}
            />
          </div>
        </div>
      }
    />
  );
}
