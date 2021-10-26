import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';

const itemName = 'loại chi phí';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'name',
      label: 'Loại chi phí',
      type: 'input'
    },
    {
      name: 'description',
      label: 'Mô tả',
      type: 'textarea',
      attrs: {rows: 2}
    },
  ],
  detailUrl: '/accounting/expense-type/crud/[$id$]',
  createUrl: '/accounting/expense-type/crud/',
  updateUrl: '/accounting/expense-type/crud/[$id$]/'
};

export default function ExpenseTypeForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../expenseType';
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
