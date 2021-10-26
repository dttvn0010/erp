import { useRouter } from 'next/router';
import { useEffect } from 'react';

import Card from 'components/share/card';
import Input from 'components/share/input';
import ErrorList from 'components/share/errorlist';

import { 
  IconLink, 
  IconButton,
  useSliceStore,
  useSliceSelector,
  copyArray
} from 'utils/helper';

import { NAME_SPACE } from 'redux/reducers/accounting/expense/formReducer';

const itemName = 'chi phí';

export default function ExpenseForm({id, update, readOnly}){
  const backUrl = (update || readOnly)? '../' : '../expense';
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
      axios.get(`${baseUrl}/detail/${id}`).then(result => {
        store.setState({data: result.data});
      });
    }
  }, [id]);

  const updateData = newData => {
    const data = store.getState().data ?? {};
    
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

  const saveExpense = async (e) => {
    e.preventDefault();
    if(readOnly) return; 

    const {data} = store.getState();

    try{
      await axios.post(`${baseUrl}/save`, data);
      router.push(backUrl);
    }catch(err){
      store.setState({
        errors: err?.response?.data ?? {}
      });
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

  let ncol = 5;
  if(readOnly) ncol -= 1;

  return (
    <Card
      title={title}
      body={
        <form id="fmt" onSubmit={saveExpense}>
          <div className="row">
            <div className="col-6 form-group">
              <label className="form-label text-bold">Tên chi phí:</label>
              <Input 
                type="input"
                value={data.note}
                onChange={val => updateData({note: val})}
              />
              <ErrorList errors={errors.note}/>
            </div>
            <div className="col-6 form-group">
              <label className="form-label text-bold">Hình thức thanh toán:</label>
              <div className="row">
                <div class="col-4">
                  <input 
                    type="radio" 
                    name="cash" 
                    checked={data.cash}
                    onClick={() => updateData({cash: true})}
                  /> Tiền mặt
                </div>

                <div class="col-4">
                  <input 
                    type="radio" 
                    name="cash" 
                    check={!data.cash}
                    onClick={() => updateData({cash: false})}
                  /> Chuyển khoản
                </div>
              </div>
              <ErrorList errors={errors.cash}/>
            </div>
          </div>

          {data.cash === false &&
            <div className="row mt-3">
              <div className="col-6 form-group">
                <label className="form-label text-bold">Số tài khoản gửi tiền:</label>
                <Input type="async-select"
                  optionsUrl='/accounting/search-bank-account'
                  resultDisplayFunc={item => item.account_number}
                  optionDisplayFunc={item => `${item.account_number} - ${item.bank} - ${item.account_holder}`}
                  value={data.from_bank_account}
                  onChange={val => updateData({from_bank_account: val})}
                />
                <ErrorList errors={errors.from_bank_account}/>
              </div>
              <div className="col-6 form-group">
                <label className="form-label text-bold">Số tài khoản nhận tiền:</label>
                <Input type="async-select"
                  optionsUrl='/accounting/search-bank-account'
                  resultDisplayFunc={item => item.account_number}
                  optionDisplayFunc={item => `${item.account_number} - ${item.bank} - ${item.account_holder}`}
                  value={data.to_bank_account}
                  onChange={val => updateData({to_bank_account: val})}
                />
                <ErrorList errors={errors.to_bank_account}/>
              </div>
            </div>
          }

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
                <th style={{width: "20%"}}>Loại chi phí</th>
                <th style={{width: "20%"}}>Số tiền</th>
                <th style={{width: "20%"}}>Chuyển vào tài khoản</th>
                <th style={{width: "35%"}}>Ghi chú</th>
              </tr>
            </thead>
            <tbody>
              {items.length === 0 &&
                <tr>
                  <td colSpan={ncol}>
                    Chưa có chi phí
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
                      value={item.type}
                      onChange={val => updateItem(index, {type: val})}
                      optionsUrl="/accounting/expense/search-expense-type"
                      labelField="name"
                    />
                    <ErrorList errors={errors[`items[${index}]`]?.type}/>
                  </td>
                  <td>
                    <Input
                      type="number"
                      readOnly={readOnly}
                      value={item.amount}
                      onChange={val => updateItem(index, {amount: val})}
                    />
                    <ErrorList errors={errors[`items[${index}]`]?.amount}/>
                  </td>
                  <td>
                    <Input
                      type="async-select"
                      readOnly={readOnly}
                      value={item.account}
                      onChange={val => updateItem(index, {account: val})}
                      optionsUrl="/accounting/search-account"
                      resultDisplayFunc={item => item.code}
                      optionDisplayFunc={item => `${item.code} - ${item.name}`}
                    />
                    <ErrorList errors={errors[`items[${index}]`]?.account}/>
                  </td>
                  <td>
                    <Input
                      type="input"
                      readOnly={readOnly}
                      value={item.note}
                      onChange={val => updateItem(index, {note: val})}
                    />
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