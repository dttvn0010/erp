import ErrorList from "components/share/errorlist";
import Input from "components/share/input";
import { NAME_SPACE } from "redux/reducers/purchase/voucher/formReducer";
import { useSliceStore, useSliceSelector } from "utils/helper";

export default function Invoice({readOnly, invoiceReadOnly}) {
  const store = useSliceStore(NAME_SPACE);
  const [data, errors] = useSliceSelector(NAME_SPACE, ['data', 'errors']);
  
  const updateData = newData => {
    const data = store.getState().data ?? {};
    
    store.setState({
      data: {
        ...data,
        ...newData
      }
    }) 
  }

  return(
    <div className="row">
      <div className="col-8 p-2">
        <div className="section-title">Thông tin chung</div>
        <hr className="mt-0"/>
        <table className="table">
          <tbody>
            <tr>
              <th style={{width: '30%'}}>Nhà cung cấp:</th>
              <td>
                <Input
                  type="async-select"
                  readOnly={readOnly}
                  value={data.supplier}
                  onChange={(val) => updateData({supplier: val})}
                  optionsUrl="/purchase/search-supplier"
                  labelField="name"
                />
                <ErrorList errors={errors.supplier}/>
              </td>
            </tr>

            <tr>
              <th>Địa chỉ:</th>
              <td>
                <Input
                  type="textarea"
                  rows="3"
                  readOnly={readOnly}
                  value={data.supplier_address}
                  onChange={val => updateData({supplier_address: val})}
                />
              </td>
            </tr>

            <tr>
              <th>Mã số thuế:</th>
              <td>
                <Input
                  type="input"
                  readOnly={readOnly}
                  value={data.supplier_tax_number}
                  onChange={val => updateData({supplier_tax_number: val})}
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div className="col-4 p-2">
        <div className="section-title">Hoá đơn</div>
        <hr className="mt-0"/>
        <table className="table">
          <tbody>
            <tr>
              <th style={{width: '35%'}}>Mẫu số hoá đơn:</th>
              <td>
                <Input
                  type="input"
                  readOnly={readOnly || invoiceReadOnly}
                  value={data.invoice_template}
                  onChange={val => updateData({invoice_template: val})}
                />
              </td>
            </tr>
            <tr>
              <th style={{width: '35%'}}>Ký hiệu hoá đơn:</th>
              <td>
                <Input
                  type="input"
                  readOnly={readOnly || invoiceReadOnly}
                  value={data.invoice_notation}
                  onChange={val => updateData({invoice_notation: val})}
                />
              </td>
            </tr>
            <tr>
              <th style={{width: '35%'}}>Số hoá đơn:</th>
              <td>
                <Input
                  type="input"
                  readOnly={readOnly || invoiceReadOnly}
                  value={data.invoice_number}
                  onChange={val => updateData({invoice_number: val})}
                />
              </td>
            </tr>
            
            <tr>
              <th>Ngày hoá đơn:</th>
              <td>
                <Input
                  type="date"
                  readOnly={readOnly||invoiceReadOnly}
                  value={data.invoice_date}
                  onChange={val => updateData({invoice_date: val})}
                />
              </td>
            </tr>
            
          </tbody>
        </table>
      </div>
    </div>
  )
}