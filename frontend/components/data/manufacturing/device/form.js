import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';

const itemName = 'thiết bị';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'workcenter',
      label: 'Phân xưởng',
      type: 'async-select',
      attrs:{
        optionsUrl: '/mfr/device/search-work-center',
        labelField: 'name'
      }
    },
    {
      name: '_class',
      label: 'Lớp thiết bị',
      type: 'async-select',
      attrs:{
        optionsUrl: '/mfr/device/search-device-class',
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
  detailUrl: '/mfr/device/crud/[$id$]',
  createUrl: '/mfr/device/crud/',
  updateUrl: '/mfr/device/crud/[$id$]/'
};

export default function DeviceForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../device';
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
