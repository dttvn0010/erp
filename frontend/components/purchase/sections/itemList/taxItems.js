import Input from 'components/share/input';

import { 
  useSliceStore, 
  useSliceSelector,
  copyArray,
} from 'utils/helper';

import { NAME_SPACE } from "redux/reducers/purchase/voucher/formReducer";

export default function TaxItems({readOnly}) {
  const store = useSliceStore(NAME_SPACE);
  const [data] = useSliceSelector(NAME_SPACE, ['data', 'errors']);
  const items = data.items || [];

  const updateItem = (index, itemData) => {
    const {data} = store.getState();
    const items = copyArray(data.items) || [];
    items[index] = {...items[index], ...itemData};
    store.setState({data: {...data, items}});
  }

  const getTotal = (item) => {
    if(item.price_unit && item.qty) {
      return item.price_unit * item.qty;
    }
  }

  const getVAT = (item) => {
    const total = getTotal(item);
    if(item.vat_rate && total){
      return Math.round(total * item.vat_rate/100);
    }
  }
  
  return(
    <>
      <table className="table mt-3" style={{width: "100%"}}>
        <thead>
          <tr>
            <th style={{width: '20%'}}>
              Hàng hoá/dịch vụ
            </th>
            <th style={{width: '10%'}}>Số tiền</th>
            <th style={{width: '25%'}}>Diễn giải thuế</th>
            <th style={{width: '7%'}}>% thuế GTGT</th>
            <th style={{width: '10%'}}>Tiền thuế GTGT</th>
            <th style={{width: '7%'}}>TK thuế GTGT</th>
            <th style={{width: '20%'}}>Nhóm HHDV mua vào</th>
          </tr>
        </thead>
        <tbody>
          {items.length === 0 &&
            <tr>
              <td colSpan="7">
                Chưa có hàng hoá/dịch vụ
              </td>
            </tr>
          }
          {items.map((item, index) => 
            <tr key={index}>
              <td>
                <span>{item.product?.name}</span>
              </td>

              <td>
                <span>{getTotal(item)}</span>
              </td>

              <td>
                <Input
                  type="input"
                  readOnly={readOnly}
                  value={item.tax_note}
                  onChange={val => updateItem(index, {tax_note: val})}
                />
              </td>

              <td>
                <Input
                  type="number"
                  readOnly={readOnly}
                  value={item.vat_rate}
                  onChange={val => updateItem(index, {vat_rate: val})}
                  min="0"
                />
              </td>
              <td>
                <span>{getVAT(item)}</span>
              </td>
              <td>
                <Input
                  type="input"
                  readOnly={readOnly}
                  value={item.tax_account}
                  onChange={val => updateItem(index, {tax_account: val})}
                />
              </td>
              <td>
                <Input
                  type="input"
                  readOnly={readOnly}
                  value={item.category}
                  onChange={val => updateItem(index, {category: val})}
                />
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </>
  )
}