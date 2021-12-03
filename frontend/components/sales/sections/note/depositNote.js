import ErrorList from "components/share/errorlist";
import Input from "components/share/input";
import { NAME_SPACE } from "redux/reducers/sales/formReducer";
import { useSliceStore, useSliceSelector } from "utils/helper";

export default function DepositNote({readOnly}) {
  const store = useSliceStore(NAME_SPACE);
  const [data, errors] = useSliceSelector(NAME_SPACE, ['data', 'errors']);
  
  const updateData = newData => {
    for(let [k,v] of Object.entries(newData)) {
      if(k.endsWith('_obj')) newData[k.replace('_obj', '')] = v?.id;
    }

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
          <ErrorList errors={errors?.order_number}/>
        </div>
        <div className="col-4 form-group">
          <label className="form-label text-bold">Tài khoản chuyển tiền:</label>
          <Input
            type="async-select"
            readOnly={readOnly}
            value={data.from_bank_account_obj}
            onChange={val => updateData({from_bank_account_obj: val})}
            optionsUrl="/sales/search-bank-account"
            labelField="name"
          />
          <ErrorList errors={errors?.from_bank_account}/>
        </div>
        <div className="col-4 form-group">
          <label className="form-label text-bold">Tài khoản nhận:</label>
          <Input
            type="async-select"
            readOnly={readOnly}
            value={data.to_bank_account_obj}
            onChange={val => updateData({to_bank_account_obj: val})}
            optionsUrl="/sales/search-bank-account"
            labelField="name"
          />
          <ErrorList errors={errors?.to_bank_account}/>
        </div>
      </div>
      <div className="row mt-2">
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
          <label className="form-label text-bold">Ngày chứng từ:</label>
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