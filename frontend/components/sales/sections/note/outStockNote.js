import ErrorList from "components/share/errorlist";
import Input from "components/share/input";
import { NAME_SPACE } from "redux/reducers/sales/formReducer";
import { useSliceStore, useSliceSelector } from "utils/helper";

export default function OutStockNote({readOnly}) {
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
          <label className="form-label text-bold">Số phiếu xuất:</label>
          <Input
            type="input"
            readOnly={readOnly}
            value={data.export_number}
            onChange={val => updateData({export_number: val})}
          />
          <ErrorList errors={errors?.export_number}/>
        </div>
        <div className="col-4 form-group">
          <label className="form-label text-bold">Ngày xuất:</label>
          <Input
            type="datetime"
            readOnly={readOnly}
            value={data.export_date}
            onChange={val => updateData({export_date: val})}
          />
          <ErrorList errors={errors?.export_date}/>
        </div>
      </div>
      <div className="row mt-2">
        <div className="col">
          <label className="form-label text-bold">Ghi chú:</label>
          <Input
            type="textarea"
            rows="3"
            readOnly={readOnly}
            value={data.export_note}
            onChange={val => updateData({export_note: val})}
          />
          <ErrorList errors={errors?.export_note}/>
        </div>
      </div>
    </div>
  )
}