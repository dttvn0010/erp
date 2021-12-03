import ErrorList from "components/share/errorlist";
import Input from "components/share/input";
import { NAME_SPACE } from "redux/reducers/purchase/formReducer";
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
    <div className="p-1">
      <div className="row mt-2">
        <div className="col-4 form-group">
          <label className="form-label text-bold">Số đơn hàng:</label>
          <Input
            type="input"
            readOnly={readOnly}
            value={data.order_number}
            onChange={val => updateData({order_number: val})}
          />
          <ErrorList errors={errors?.order_number}/>
        </div>
        <div className="col-4 form-group">
          <label className="form-label text-bold">Ngày hạch toán:</label>
          <Input
            type="datetime"
            readOnly={readOnly}
            value={data.accounting_date}
            onChange={val => updateData({accounting_date: val})}
          />
          <ErrorList errors={errors?.accounting_date}/>
        </div>
        <div className="col-4 form-group">
          <label className="form-label text-bold">Ngày thực hiện:</label>
          <Input
            type="datetime"
            readOnly={readOnly}
            value={data.order_date}
            onChange={val => updateData({order_date: val})}
          />
          <ErrorList errors={errors?.order_date}/>
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
          <ErrorList errors={errors?.note}/>
        </div>
      </div>
    </div>
  )
}