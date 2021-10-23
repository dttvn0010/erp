import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';

const itemName = 'loại thu tiền';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'name',
      label: 'Loại thu tiền',
      type: 'input'
    },
    {
      name: 'description',
      label: 'Mô tả',
      type: 'textarea',
      attrs: {rows: 2}
    },
  ],
  detailUrl: '/accounting/income-type/crud/[$id$]',
  createUrl: '/accounting/income-type/crud/',
  updateUrl: '/accounting/income-type/crud/[$id$]/'
};

export default function IncomeTypeForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../income-type';
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
