import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';

const itemName = 'lớp thiết bị';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'category',
      label: 'Nhóm thiết bị',
      type: 'async-select',
      attrs:{
        optionsUrl: '/mfr/device-class/search-category',
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
    {
      name: 'hours_to_be_maintained',
      label: 'Số giờ hoạt động mỗi lần bảo trì',
      type: 'number',
      attrs: {
        min: 0
      }
    },
  ],
  detailUrl: '/mfr/device-class/crud/[$id$]',
  createUrl: '/mfr/device-class/crud/',
  updateUrl: '/mfr/device-class/crud/[$id$]/'
};

export default function DeviceClassForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../deviceClass';
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
