import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';

const itemName = 'nhóm thiết bị';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'device',
      label: 'Thiết bị',
      type: 'async-select',
      attrs:{
        optionsUrl: '/mfr/device-maintainance/search-device',
        labelField: 'name'
      }
    },
    {
      name: 'planned_start_date',
      label: 'Thời gian bắt đầu',
      type: 'datetime'
    },
    {
      name: 'planned_end_date',
      label: 'Thời gian kết thúc',
      type: 'datetime'
    },
  ],
  detailUrl: '/mfr/device-maintainance/crud/[$id$]',
  createUrl: '/mfr/device-maintainance/crud/',
  updateUrl: '/mfr/device-maintainance/crud/[$id$]/'
};

export default function DeviceMaintainanceForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../deviceMaintainance';
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
