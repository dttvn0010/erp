import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';

const itemName = 'nhóm thiết bị';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'parent',
      label: 'Nhóm cha',
      type: 'async-select',
      attrs:{
        optionsUrl: '/mfr/device-category/search-parent',
        labelField: 'name'
      }
    },
    {
      name: 'code',
      label: 'Mã',
      type: 'input'
    },
    {
      name: 'name',
      label: 'Tên',
      type: 'input'
    },
  ],
  detailUrl: '/mfr/device-category/crud/[$id$]',
  createUrl: '/mfr/device-category/crud/',
  updateUrl: '/mfr/device-category/crud/[$id$]/'
};

export default function DeviceCategoryForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../deviceCategory';
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
