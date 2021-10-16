import ErrorList from "components/share/errorlist";
import Input from "components/share/input";
import { NAME_SPACE } from "redux/reducers/purchase/voucher/formReducer";
import { useSliceStore, useSliceSelector } from "utils/helper";

export default function ExpenseNote({readOnly}) {
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
              <th>Người nhận:</th>
              <td>
                <Input
                  type="input"
                  readOnly={readOnly}
                  value={data.payee}
                  onChange={val => updateData({payee: val})}
                />
              </td>
            </tr>
            <tr>
              <th>Địa chỉ:</th>
              <td>
                <Input
                  type="textarea"
                  rows="2"
                  readOnly={readOnly}
                  value={data.payee_address}
                  onChange={val => updateData({payee_address: val})}
                />
              </td>
            </tr>
            <tr>
              <th>Lý do chi:</th>
              <td>
                <Input
                  type="textarea"
                  rows="2"
                  readOnly={readOnly}
                  value={data.detail}
                  onChange={val => updateData({detail: val})}
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div className="col-4 p-2">
        <div className="section-title">Chứng từ</div>
        <hr className="mt-0"/>
        <table className="table">
          <tbody>
            <tr>
              <th style={{width: '35%'}}>Ngày hạch toán:</th>
              <td>
                <Input
                  type="date"
                  readOnly={readOnly}
                  value={data.acc_date}
                  onChange={val => updateData({acc_date: val})}
                />
              </td>
            </tr>
            <tr>
              <th>Ngày chứng từ:</th>
              <td>
                <Input
                  type="date"
                  readOnly={readOnly}
                  value={data.ca_date}
                  onChange={val => updateData({ca_date: val})}
                />
              </td>
            </tr>
            <tr>
              <th>Số chứng từ:</th>
              <td>
                <Input
                  type="input"
                  readOnly={readOnly}
                  value={data.payement_number}
                  onChange={val => updateData({payement_number: val})}
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}