import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';

const itemName = 'hàng hoá/dịch vụ';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'category',
      displayField: 'category_name',
      label: 'Nhóm',
      type: 'async-select',
      options: {
        url: '/stock/product/search-category',
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
      name: 'description',
      label: 'Mô tả',
      type: 'textarea',
      attrs: {rows: 5}
    },
    {
      name: 'list_price',
      label: 'Giá chuẩn',
      type: 'number',
      attrs: {min: 0, step: 1000}
    }
  ],
  detailUrl: '/stock/product/api/crud/[$id$]',
  createUrl: '/stock/product/api/crud/',
  updateUrl: '/stock/product/api/crud/[$id$]/'
};

export default function ProductForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../product';
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
