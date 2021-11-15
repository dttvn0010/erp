import ErrorList from "components/share/errorlist";
import Input from "components/share/input";
import { NAME_SPACE } from "redux/reducers/purchase/voucher/formReducer";
import { useSliceStore, useSliceSelector } from "utils/helper";

export default function ReceiptNote({readOnly}) {
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
          <label className="form-label text-bold">Số phiếu thu:</label>
          <Input
            type="input"
            readOnly={readOnly}
            value={data.receipt_number}
            onChange={val => updateData({receipt_number: val})}
          />
        </div>
        <div className="col-4 form-group">
          <label className="form-label text-bold">Ngày hạch toán:</label>
          <Input
            type="date"
            readOnly={readOnly}
            value={data.acc_date}
            onChange={val => updateData({acc_date: val})}
          />
        </div>
        <div className="col-4 form-group">
          <label className="form-label text-bold">Ngày chứng từ:</label>
          <Input
            type="date"
            readOnly={readOnly}
            value={data.ca_date}
            onChange={val => updateData({ca_date: val})}
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
            value={data.detail}
            onChange={val => updateData({detail: val})}
          />
        </div>
      </div>
    </div>
  )
}