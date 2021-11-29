import ErrorList from "components/share/errorlist";
import Input from "components/share/input";
import { NAME_SPACE } from "redux/reducers/sales/voucher/formReducer";
import { useSliceStore, useSliceSelector } from "utils/helper";

export default function DepositNote({readOnly}) {
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
    <div className="p-1">
      <div className="row mt-2">
        <div className="col-4 form-group">
          <label className="form-label text-bold">Số chứng từ:</label>
          <Input
            type="input"
            readOnly={readOnly}
            value={data.order_number}
            onChange={val => updateData({order_number: val})}
          />
        </div>
        <div className="col-4 form-group">
          <label className="form-label text-bold">Tài khoản chuyển tiền:</label>
          <Input
            type="async-select"
            readOnly={readOnly}
            value={data.from_bank_account}
            onChange={val => updateData({from_bank_account: val})}
            optionsUrl="/sales/search-bank-account"
            labelField="name"
          />
        </div>
        <div className="col-4 form-group">
          <label className="form-label text-bold">Tài khoản nhận:</label>
          <Input
            type="async-select"
            readOnly={readOnly}
            value={data.to_bank_account}
            onChange={val => updateData({to_bank_account: val})}
            optionsUrl="/sales/search-bank-account"
            labelField="name"
          />
        </div>
      </div>
      <div className="row mt-2">
        <div className="col-4 form-group">
          <label className="form-label text-bold">Ngày hạch toán:</label>
          <Input
            type="date"
            readOnly={readOnly}
            value={data.accouting_date}
            onChange={val => updateData({accouting_date: val})}
          />
        </div>
        <div className="col-4 form-group">
          <label className="form-label text-bold">Ngày chứng từ:</label>
          <Input
            type="date"
            readOnly={readOnly}
            value={data.order_date}
            onChange={val => updateData({order_date: val})}
          />
        </div>
      </div>
      <div className="row mt-2">
        <div className="col">
          <label className="form-label text-bold">Ghi chú:</label>
          <Input
            type="textarea"
            rows="3"
            readOnly={readOnly}
            value={data.note}
            onChange={val => updateData({note: val})}
          />
        </div>
      </div>
    </div>
  )
}