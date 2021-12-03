import ErrorList from "components/share/errorlist";
import Input from "components/share/input";
import { NAME_SPACE } from "redux/reducers/purchase/formReducer";
import { useSliceStore, useSliceSelector } from "utils/helper";

export default function Invoice({readOnly}) {
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
          <label className="form-label text-bold">Mẫu hoá đơn:</label>
          <Input
            type="input"
            readOnly={readOnly}
            value={data.invoice_type}
            onChange={val => updateData({invoice_type: val})}
          />
        </div>
        <div className="col-4 form-group">
          <label className="form-label text-bold">Số hoá đơn:</label>
          <Input
            type="input"
            readOnly={readOnly}
            value={data.invoice_number}
            onChange={val => updateData({invoice_number: val})}
          />
          <ErrorList errors={errors?.invoice_number}/>
        </div>
        <div className="col-4 form-group">
          <label className="form-label text-bold">Ngày hoá đơn:</label>
          <Input
            type="datetime"
            readOnly={readOnly}
            value={data.invoice_date}
            onChange={val => updateData({invoice_date: val})}
          />
          <ErrorList errors={errors?.invoice_date}/>
        </div>
      </div>
      <div className="row mt-2">
        <div className="col">
          <label className="form-label text-bold">Ghi chú:</label>
          <Input
            type="textarea"
            rows="3"
            readOnly={readOnly}
            value={data.invoice_note}
            onChange={val => updateData({invoice_note: val})}
          />
          <ErrorList errors={errors?.invoice_note}/>
        </div>
      </div>
    </div>
  )
}