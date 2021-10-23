import ErrorList from "components/share/errorlist";
import Input from "components/share/input";
import { NAME_SPACE } from "redux/reducers/purchase/voucher/formReducer";
import { useSliceStore, useSliceSelector } from "utils/helper";

export default function DebtDeductNote({readOnly}) {
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
              <th>Diễn giải:</th>
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

            <tr>
              <th>Nhân viên mua hàng:</th>
              <td>
                <Input
                  type="async-select"
                  readOnly={readOnly}
                  value={data.purchase_person}
                  onChange={val => updateData({purchase_person: val})}
                  optionsUrl="/purchase/search-employee"
                  labelField="name"
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
                  value={data.debt_deduct_number}
                  onChange={val => updateData({debt_deduct_number: val})}
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}