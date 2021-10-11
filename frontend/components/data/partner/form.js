import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';

const itemName = 'khách hàng/nhà cung cấp';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'name',
      label: 'Tên',
      type: 'input'
    },
    {
      name: 'phone',
      label: 'Số điện thoại',
      type: 'input'
    },
    {
      name: 'email',
      label: 'Email',
      type: 'input'
    },
    {
      name: 'address',
      label: 'Địa chỉ',
      type: 'textarea',
      attrs: {rows: 2}
    },
    {
      name: 'is_supplier',
      label: 'Là nhà cung cấp',
      type: 'checkbox',
    },
    {
      name: 'is_customer',
      label: 'Là khách hàng',
      type: 'checkbox',
    },
    {
      name: 'is_agent',
      label: 'Là đại lý',
      type: 'checkbox',
    }
  ],
  detailUrl: '/partner/crud/[$id$]',
  createUrl: '/partner/crud/',
  updateUrl: '/partner/crud/[$id$]/'
};

export default function PartnerForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../partner';
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
