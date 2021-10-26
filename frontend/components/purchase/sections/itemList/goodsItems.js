import Input from 'components/share/input';
import ErrorList from 'components/share/errorlist';

import { 
  useSliceStore, 
  useSliceSelector,
  copyArray,
} from 'utils/helper';

import { NAME_SPACE } from "redux/reducers/purchase/voucher/formReducer";

export default function GoodItems({readOnly, toStock, paymentType}) {
  const store = useSliceStore(NAME_SPACE);
  const [data, errors] = useSliceSelector(NAME_SPACE, ['data', 'errors']);
  const items = data.items || [];

  const addItem = (index) => {
    const {data} = store.getState();
    const items = copyArray(data.items) || [];
  
    if(index == -1) {
      items.push({qty: 1});
    }else{
      items.splice(index+1, 0, {qty: 1});
    }
  
    store.setState({data: {...data, items}});
  }

  const updateItem = (index, itemData) => {
    const {data} = store.getState();
    const items = copyArray(data.items) || [];
    items[index] = {...items[index], ...itemData};
    store.setState({data: {...data, items}});
  }

  const changeProduct = (index, val) => {
    updateItem(index, {
      product: val,
      unit: val.unit,
      price_unit: val.price_unit
    })
  }

  const deleteItem = (index) => {
    const {data} = store.getState();
    const items = copyArray(data.items) || [];
    items.splice(index, 1);
    store.setState({data: {...data, items}});
  }

  const getTotal = (item) => {
    if(item.price_unit && item.qty) {
      return item.price_unit * item.qty;
    }
  }

  const getDiscount = (item) => {
    const total = getTotal(item);
    if(item.discount_rate && total){
      return Math.round(total * item.discount_rate/100);
    }
  }

  const getNet = (item) => {
    let total = getTotal(item);
    const discount = getDiscount(item);
    if(total && discount) total -= discount;
    return total;
  }

  let ncol = 11;
  if(readOnly) ncol -= 1;
  
  return(
    <div style={{overflow: "auto", minHeight: "200px"}}>
      <table className="table mt-3" style={{width: "120%"}}>
        <thead>
          <tr>
            {!readOnly &&
              <th className="text-center">
                <a className="ms-3" href='#/' onClick={() => addItem(-1)}>
                  <i className="fas fa-plus"></i>
                </a>
              </th>
            }
            <th style={{width: '20%'}}>
              Hàng hoá/dịch vụ
            </th>
            <th style={{width: '7%'}}>
              {toStock && <>Kho</>}
              {!toStock && <>TK Chi phí</>}
            </th>
            <th style={{width: '7%'}}>
              {paymentType && <>TK tiền</>}
              {!paymentType && <>TK công nợ</>}
            </th>
            <th style={{width: '10%'}}>Đơn giá</th>
            <th style={{width: '7%'}}>Số lượng</th>
            <th style={{width: '7%'}}>Đơn vị</th>
            <th style={{width: '10%'}}>Thành tiền</th>
            <th style={{width: '7%'}}>CK (%)</th>
            <th style={{width: '10%'}}>Tiền CK</th>
            <th style={{width: '10%'}}>Giá trị</th>
          </tr>
        </thead>
        <tbody>
          {items.length === 0 &&
            <tr>
              <td colSpan={ncol}>
                Chưa có hàng hoá/dịch vụ
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
                  value={item.product}
                  onChange={(val) => changeProduct(index, val)}
                  optionsUrl="/purchase/search-product"
                  labelField="name"
                />
                <ErrorList errors={errors[`items[${index}]`]?.product}/>
              </td>

              <td>
                {toStock &&
                  <Input
                    type="input"
                    readOnly={readOnly}
                    value={item.stock}
                    onChange={val => updateItem(index, {stock: val})}
                  />
                }
                {!toStock &&
                  <Input
                    type="input"
                    readOnly={readOnly}
                    value={item.expense_account}
                    onChange={val => updateItem(index, {expense_account: val})}
                  />
                }
              </td>

              <td>
                {!paymentType && 
                  <Input
                    type="input"
                    readOnly={readOnly}
                    value={item.debt_account}
                    onChange={val => updateItem(index, {debt_account: val})}
                  />
                }
                {paymentType === 'cash' && 
                  <Input
                    type="input"
                    readOnly={readOnly}
                    value={item.cash_account}
                    onChange={val => updateItem(index, {cash_account: val})}
                  />
                }
                {paymentType === 'bank' && 
                  <Input
                    type="input"
                    readOnly={readOnly}
                    value={item.cash_account}
                    onChange={val => updateItem(index, {bank_account: val})}
                  />
                }
              </td>

              <td>
                <Input
                  type="number"
                  readOnly={readOnly}
                  value={item.price_unit}
                  onChange={val => updateItem(index, {price_unit: val})}
                  min="0"
                />
                <ErrorList errors={errors[`items[${index}]`]?.price_unit}/>
              </td>
              
              <td>
                <Input
                  type="number"
                  readOnly={readOnly}
                  value={item.qty}
                  onChange={val => updateItem(index, {qty: val})}
                  min="1"
                />
                <ErrorList errors={errors[`items[${index}]`]?.qty}/>
              </td>

              <td>
                <span>{item.unit}</span>
              </td>

              <td>
                <span>{getTotal(item)}</span>
              </td>
              <td>
                <Input
                  type="number"
                  readOnly={readOnly}
                  value={item.discount_rate}
                  onChange={val => updateItem(index, {discount_rate: val})}
                  min="0"
                />
              </td>
              <td>
                <span>{getDiscount(item)}</span>
              </td>
              <td>
                <span>{getNet(item)}</span>
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}