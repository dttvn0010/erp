import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';

const itemName = 'phòng/ban';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'name',
      label: 'Tên',
      type: 'input'
    },
    {
      name: 'parent',
      displayField: 'parent_name',
      label: 'Trực thuộc',
      type: 'async-select',
      options: {
        url: '/employee/department/search-parent',
        getExtraParams : (id, _) => ({instanceId: id}),
        labelField: 'name'
      }
    },
    {
      name: 'manager',
      displayField: 'manager_name',
      label: 'Người quản lý',
      type: 'async-select',
      options: {
        url: '/employee/department/search-employee',
        labelField: 'name'
      }
    },
    
  ],
  detailUrl: '/employee/department/crud/[$id$]',
  createUrl: '/employee/department/crud/',
  updateUrl: '/employee/department/crud/[$id$]/'
};

export default function StockForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../department';
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
