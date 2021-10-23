import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';

const itemName = 'ngân hàng';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'code',
      label: 'Tên viết tắt',
      type: 'input'
    },
    {
      name: 'name',
      label: 'Tên đầy đủ',
      type: 'input'
    },
    {
      name: 'logo',
      label: 'Logo',
      type: 'file'
    }
  ],
  detailUrl: '/accounting/bank/crud/[$id$]',
  createUrl: '/accounting/bank/crud/',
  updateUrl: '/accounting/bank/crud/[$id$]/'
};

export default function BankForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../bank';
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
