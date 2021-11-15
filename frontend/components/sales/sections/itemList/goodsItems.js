import Input from 'components/share/input';
import ErrorList from 'components/share/errorlist';

import { 
  useSliceStore, 
  useSliceSelector,
  copyArray,
} from 'utils/helper';

import { NAME_SPACE } from "redux/reducers/sales/voucher/formReducer";

export default function GoodItems({readOnly, withStock, withDiscount, withTax}) {
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
      unit: val?.unit,
      price_unit: val?.price_unit
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

  const getVAT = (item) => {
    const total = getTotal(item);
    if(item.vat_rate && total){
      return Math.round(total * item.vat_rate/100);
    }
  }

  const getNet = (item) => {
    let net = getTotal(item);
    let vat = getVAT(item);
    const discount = getDiscount(item);
    if(net && discount) net -= discount;
    if(net && vat) net += vat;
    return net;
  }

  let ncol = 12;
  if(readOnly) ncol -= 1;
  if(!withStock) ncol -= 1;
  if(!withTax) ncol -= 2;
  if(!withDiscount) ncol -= 2;
  if(!withTax && !withDiscount) ncol -= 1;
  
  return(
    <div style={{overflow: "auto", minHeight: "200px"}}>
      <table className="table mt-3" style={{width: "120%"}}>
        <thead>
          <tr>
            {!readOnly &&
              <th className="text-center" style={{width: '4%'}}>
                <a className="ms-3" href='#/' onClick={() => addItem(-1)}>
                  <i className="fas fa-plus"></i>
                </a>
              </th>
            }
            <th style={{width: '18%'}}>
              Hàng hoá/dịch vụ
            </th>
            {withStock && 
              <th style={{width: '12%'}}>
                Lấy từ kho
              </th>
            }
            <th style={{width: '8%'}}>Đơn giá</th>
            <th style={{width: '8%'}}>Số lượng</th>
            <th style={{width: '8%'}}>Đơn vị</th>
            {(withTax || withDiscount) && <th style={{width: '8%'}}>Thành tiền</th>}
            {withDiscount && <th style={{width: '5%'}}>% CK</th>}
            {withDiscount && <th style={{width: '8%'}}>Tiền CK</th>}
            {withTax && <th style={{width: '5%'}}>% Thuế GTGT</th>}
            {withTax && <th style={{width: '8%'}}>Tiền thuế GTGT</th>}
            <th style={{width: '8%'}}>Giá trị thanh toán</th>
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
                    <a className="me-3" href='#/' onClick={() => deleteItem(index)}>
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
                  optionsUrl="/sales/search-product"
                  labelField="name"
                />
                <ErrorList errors={errors[`items[${index}]`]?.product}/>
              </td>

              {withStock &&
                <td>
                  <Input
                    type="async-select"
                    readOnly={readOnly}
                    value={item.stock}
                    onChange={val => updateItem(index, {stock: val})}
                    optionsUrl="/sales/search-stock-location"
                    labelField="name"
                  />
                </td>
              }
            
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

              { (withTax || withDiscount) &&
                <td>
                  <span>{getTotal(item)}</span>
                </td>
              }

              {withDiscount &&
                <td>
                  <Input
                    type="number"
                    readOnly={readOnly}
                    value={item.discount_rate}
                    onChange={val => updateItem(index, {discount_rate: val})}
                    min="0"
                  />
                </td>
              }

              {withDiscount &&
                <td>
                  <span>{getDiscount(item)}</span>
                </td>
              }

              {withTax &&
                <td>
                  <Input
                    type="number"
                    readOnly={readOnly}
                    value={item.vat_rate}
                    onChange={val => updateItem(index, {vat_rate: val})}
                    min="0"
                  />
                </td>
              }

              {withTax &&
                <td>
                  <span>{getVAT(item)}</span>
                </td>
              }

              
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