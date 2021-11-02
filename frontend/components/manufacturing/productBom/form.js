import axios from 'axios';
import { useRouter } from 'next/router';
import { useEffect } from 'react';

import Card from 'components/share/card';
import Input from 'components/share/input';
import ErrorList from 'components/share/errorlist';

import { 
  IconLink, 
  IconButton,
  Spiner,
  useSliceStore,
  useSliceSelector,
  copyArray
} from 'utils/helper';

import { NAME_SPACE } from 'redux/reducers/manufacturing/productBom/formReducer';

const itemName = 'định lượng NVL';

export default function ProductBomForm({id, update, readOnly}){
  const baseUrl = '/mfr/product-bom';
  const backUrl = (update || readOnly)? '../' : '../productBom';
  const editUrl = id? `../update/${id}` : null;
  
  const router = useRouter();
  const store = useSliceStore(NAME_SPACE);
  const [data, errors] = useSliceSelector(NAME_SPACE, ['data', 'errors']);
  const items = data.items || [];

  useEffect(() => {
    store.setState({
      data: {},
      errors: {}
    });

    if(id) {
      axios.get(`${baseUrl}/crud/${id}`).then(result => {
        store.setState({data: result.data});
      });
    }
  }, [id]);

  const updateData = newData => {
    const data = store.getState().data ?? {};
    
    for(let [k,v] of Object.entries(newData)) {
      if(k.endsWith('_obj')) newData[k.replace('_obj', '')] = v?.id;
    }

    store.setState({
      data: {
        ...data,
        ...newData
      }
    }) 
  }

  const addItem = (index) => {
    const {data} = store.getState();
    const items = copyArray(data.items) || [];
  
    if(index == -1) {
      items.push({});
    }else{
      items.splice(index+1, 0, {});
    }
    
    store.setState({data: {...data, items}});
  }

  const updateItem = (index, itemData) => {
    for(let [k,v] of Object.entries(itemData)) {
      if(k.endsWith('_obj')) itemData[k.replace('_obj', '')] = v?.id;
    }

    const {data} = store.getState();
    const items = copyArray(data.items) || [];
    items[index] = {...items[index], ...itemData};
    store.setState({data: {...data, items}});
  }

  const deleteItem = (index) => {
    const {data} = store.getState();
    const items = copyArray(data.items) || [];
    items.splice(index, 1);
    store.setState({data: {...data, items}});
  }

  const saveProductBom = async (e) => {
    e.preventDefault();
    if(readOnly) return; 

    const {data} = store.getState();

    try{
      if(update) {
        await axios.put(`${baseUrl}/crud/${id}/`, data);
      }else{
        await axios.post(`${baseUrl}/crud/`, data);
      }

      router.push(backUrl);
    }catch(err){
      store.setState({
        errors: err?.response?.data ?? {}
      });
      console.log(err?.response?.data );
      alert('Đã có lỗi xảy ra');
    }
  }

  const title = (
    readOnly? `Xem ${itemName}` : (update? `Cập nhập ${itemName}` : `Thêm ${itemName}`)
  );
  
  const loading = (update || readOnly) && !data.id;

  if(loading) {
    return(
      <div className="text-center p-3">
        <Spiner/>
      </div>
    )
  }

  let ncol = 4;
  if(readOnly) ncol -= 1;

  return (
    <Card
      title={title}
      body={
        <form id="fmt" onSubmit={saveProductBom}>
          <div className="row">
            <div className="col-6 form-group">
              <label className="form-label text-bold">Tên định lượng NVL:</label>
              <Input 
                type="input"
                value={data.name}
                onChange={val => updateData({name: val})}
                readOnly={readOnly}
              />
              <ErrorList errors={errors.name}/>
            </div>
            <div className="col-6 form-group">
              <label className="form-label text-bold">Thành phẩm:</label>
              <Input 
                type="async-select"
                value={data.product_obj}
                onChange={val => updateData({product_obj: val})}
                readOnly={readOnly}
                optionsUrl={`${baseUrl}/search-product`}
              />
              <ErrorList errors={errors.product}/>
            </div>
          </div>

          <table className="table mt-3">
            <thead>
              <tr>
                {!readOnly &&
                  <th className="text-center">
                    <a className="ms-3" href='#/' onClick={() => addItem(-1)}>
                      <i className="fas fa-plus"></i>
                    </a>
                  </th>
                }
                <th style={{width: "35%"}}>Nguyên liệu</th>
                <th style={{width: "30%"}}>Số lượng</th>
                <th style={{width: "30%"}}>Đơn vị</th>
              </tr>
            </thead>
            <tbody>
              {items.length === 0 &&
                <tr>
                  <td colSpan={ncol}>
                    Chưa có nguyên liệu
                  </td>
                </tr>
              }
              {items.map((item, index) => 
                <tr key={index}>
                  {!readOnly &&
                    <td>
                      <>
                        <a className="me-2" href='#/' onClick={() => deleteItem(index)}>
                          <i className="fas fa-trash text-danger"></i>
                        </a>
                        <a href='#/' onClick={() => addItem(index)}>
                          <i className="fas fa-plus"></i>
                        </a>
                      </>
                    </td>
                  }
                  
                  <td>
                    <Input
                      type="async-select"
                      readOnly={readOnly}
                      value={item.component_obj}
                      onChange={val => updateItem(index, {component_obj: val})}
                      optionsUrl={`${baseUrl}/search-product`}
                    />
                    <ErrorList errors={errors?.items?.[index]?.component}/>
                  </td>

                  <td>
                    <Input
                      type="number"
                      readOnly={readOnly}
                      value={item.qty}
                      onChange={val => updateItem(index, {qty: val})}
                    />
                    <ErrorList errors={errors?.items?.[index]?.qty}/>
                  </td>

                  <td>
                    <Input
                      type="input"
                      readOnly={readOnly}
                      value={item.unit}
                      onChange={val => updateItem(index, {unit: val})}
                    />
                    <ErrorList errors={errors?.items?.[index]?.unit}/>
                  </td>
                  
                </tr>
              )}
            </tbody>
          </table>
          <div className="row mt-3">
            <div className="col">
              <div>
                <IconLink 
                  href={backUrl}
                  icon="arrow-left"
                  variant="secondary"
                  title="Quay lại"
                  className="me-2"
                />
                {!readOnly &&
                  <IconButton
                    icon="save"
                    type="submit"
                    title="Lưu lại"
                  />
                }
                {readOnly && 
                  <IconLink
                    href={editUrl}
                    icon="edit"
                    title="Cập nhật"
                  />
                }
              </div>
            </div>
          </div>
        </form>
      }
    />
  )
}