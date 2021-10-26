import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';

const itemName = 'tài khoản ngân hàng';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'name',
      label: 'Tên',
      type: 'input'
    },

    {
      name: 'bank',
      label: 'Ngân hàng',
      type: 'async-select',
      attrs: {
        optionsUrl: '/accounting/bank-account/search-bank',
        labelField: 'name'
      }
    },

    {
      name: 'bank_branch',
      label: 'Chi nhánh',
      type: 'input'
    },

    {
      name: 'account_number',
      label: 'Số tài khoản',
      type: 'input'
    },

    {
      name: 'account_holder',
      label: 'Chủ tài khoản',
      type: 'input'
    },
  ],
  detailUrl: '/accounting/bank-account/crud/[$id$]',
  createUrl: '/accounting/bank-account/crud/',
  updateUrl: '/accounting/bank-account/crud/[$id$]/'
};

export default function BankAccountForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../bankAccount';
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
