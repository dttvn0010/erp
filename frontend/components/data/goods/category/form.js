import axios from 'axios';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { createForm } from 'components/share/form';
import Card from 'components/share/card';
import ErrorList from 'components/share/errorlist';
import { IconButton, IconLink } from 'utils/helper';

const itemName = 'nhóm hàng hoá/dịch vụ';

const formMeta = {
  formId: 'fmt',
  fields: [
    {
      name: 'parent',
      label: 'Nhóm cha',
      type: 'async-select',

      attrs: {
        optionsUrl: '/stock/product-category/search-parent',
        labelField: 'name',
        getParams: (id,_) => ({instanceId: id})
      },
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
    }
  ],
  detailUrl: '/stock/product-category/api/crud/[$id$]',
  createUrl: '/stock/product-category/api/crud/',
  updateUrl: '/stock/product-category/api/crud/[$id$]/'
};

export default function ProductCategoryForm({id, update, readOnly}) {
  const [form, setForm] = useState(null);
  const backUrl = (update || readOnly)? '../' : '../category';
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

function ProductCategoryForm2({id, update}) {
  const [form, setForm] = useState(null);
  const backUrl = update? '../' : '../category';
  const router = useRouter();
  const [category, setCategory] = useState({});
  const [errors, setErrors] = useState({});

  useEffect(() => {
    setForm(createForm(formMeta, update, id));
    if(id) {
      const detailUrl = formMeta.detailUrl.replace('[$id$]', id);
      axios.get(detailUrl).then(result =>
        setCategory(result.data)
      );
    }
  }, [id]);

  const saveCategory = async (e) => {
    e.preventDefault();
    const data = new FormData(document.getElementById(formMeta.formId));
    const updateUrl = formMeta.updateUrl.replace('[$id$]', id);
    const createUrl = formMeta.createUrl;

    try{
      await axios({
        method: update? 'put' : 'post',
        url: update? updateUrl : createUrl,
        data:data
      });
      router.push(backUrl);
    }catch(err){
      setErrors(err?.response?.data);
    }
  }

  if(!form) return <></>;
  const loading = update && !category.id;

  const title = (
    readOnly? `Xem ${itemName}` : (update? `Cập nhập ${itemName}` : `Tạo mới ${itemName}`)
  );

  return(
    <Card
      title={title}
      body={
        <div className="row">
          <div className="col-9">
            <form id={formMeta.formId} onSubmit={saveCategory}>
              <table className="table">
                <tbody>
                  {loading &&
                    <tr>
                      <td className="text-center">
                        <div className="spinner-border" role="status">
                          <span className="sr-only"></span>
                        </div>
                      </td>
                    </tr>
                  }
                  {!loading &&
                    <>
                      <tr>
                        <th style={{width: "30%"}}>
                          <form.Parent.Label/>
                        </th>
                        <td>
                          <form.Parent.Input itemVar={category}/>
                          <ErrorList errors={errors.parent}/>
                        </td>
                      </tr>
                      <tr>
                        <th><form.Code.Label/></th>
                        <td>
                          <form.Code.Input itemVar={category}/>
                          <ErrorList errors={errors.code}/>
                        </td>
                      </tr>
                      <tr>
                        <th><form.Name.Label/></th>
                        <td>
                          <form.Name.Input itemVar={category}/>
                          <ErrorList errors={errors.name}/>
                        </td>
                      </tr>
                      <tr>
                        <th><form.Description.Label/></th>
                        <td>
                          <form.Description.Input itemVar={category}/>
                          <ErrorList errors={errors.description}/>
                        </td>
                      </tr>
                    </>
                  }
                </tbody>
              </table>
              <div>
                <IconLink 
                  href={backUrl}
                  icon="arrow-left"
                  variant="primary"
                  title="Quay lại"
                  className="me-2"
                />
                <IconButton
                  type="submit"
                  icon="save"
                  title="Lưu lại"
                />
              </div>
            </form>
          </div>
        </div>
      }
    />
  );
}

/*
export default function ProductCategoryForm({id, update}) {
  let [state, setState] = useReducer(
    (state, newState) => ({...state, ...newState}),
    {
      errors: {},
      category: {}
    }
  );

  const router = useRouter();
  
  useEffect(() => {
    if(id) {
      axios.get(`/stock/product-category/api/detail/${id}`).then(result => {
        setState({category: result.data});
      });
    }
  }, [id]);

  const loadParentOptions = getLoadOptions({
    url: `/stock/product-category/search-parent`,
    params: { instanceId: id}, 
    labelField: "name", 
    valueField: "id"
  });

  const saveCategory = (e) => {
    e.preventDefault();
    const data = new FormData(document.getElementById("fmt"));

    if(update){
      axios.put(`/stock/product-category/api/update/${id}`, data).then(()=> {
        router.push('../')
      }).catch(err => {
        setState({errors: err.response.data})
      })
    }else{
      axios.post('/stock/product-category/api/create', data).then(() => {
        router.push('../product-category');
      }).catch(err => {
        setState({errors: err.response.data})
      })
    }
  }

  return(
    <div className="content p-3">
      <div className="card shadow mb-4">
        <div className="card-header py-3">
          <h6 className="m-0 font-weight-bold text-primary">Thêm nhóm sản phẩm</h6>
        </div>
        <div className="card-body">
          <div className="row">
            <div className="col-9">
              <form id="fmt" onSubmit={saveCategory}>
                <table className="table">
                  <tbody>
                    <tr>
                      <th style={{width: "30%"}}>Nhóm cha:</th>
                      <td>
                        <AsyncSelect
                          key={state.category.id}
                          name="parent"
                          defaultValue={{
                            label: state.category.parent_name, 
                            value: state.category.parent
                          }}
                          cacheOptions
                          loadOptions={loadParentOptions}
                          defaultOptions
                          isClearable={true}
                          placeholder=""
                        />
                        <ErrorList errors={state.errors.parent}/>
                      </td>
                    </tr>
                    <tr>
                      <th>Mã:</th>
                      <td>
                        <input 
                          name="code"
                          defaultValue={state.category.code}
                          className="form-control"
                        />
                        <ErrorList errors={state.errors.code}/>
                      </td>
                    </tr>
                    <tr>
                      <th>Tên:</th>
                      <td>
                        <input 
                          name="name"
                          defaultValue={state.category.name}
                          className="form-control"
                        />
                        <ErrorList errors={state.errors.name}/>
                      </td>
                    </tr>
                    <tr>
                      <th>Mô tả:</th>
                      <td>
                        <textarea 
                          name="description"
                          defaultValue={state.category.description}
                          rows="5"
                          className="form-control"
                        ></textarea>
                        <ErrorList errors={state.errors.description}/>
                      </td>
                    </tr>
                  </tbody>
                </table>
                
                <div>
                  <Link href={update? '../' : '../product-category'}>
                    <a className="btn btn-sm btn-secondary me-2">
                      <i className="fas fa-arrow-left text-white-50"></i> Quay lại
                    </a>
                  </Link>
                  <button type="submit" className="btn btn-sm btn-primary">
                  <i className="fas fa-save text-white-50"></i> Lưu lại
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}*/