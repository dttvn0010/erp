import Input from 'components/share/input';
import ErrorList from 'components/share/errorlist';

import { 
  useSliceStore, 
  useSliceSelector,
  copyArray,
} from 'utils/helper';

import { NAME_SPACE } from "redux/reducers/sales/formReducer";

export default function ExpenseList({readOnly}) {
  const store = useSliceStore(NAME_SPACE);
  const [data, errors] = useSliceSelector(NAME_SPACE, ['data', 'errors']);
  const expenses = data.expenses || [];

  const addExpense = (index) => {
    const {data} = store.getState();
    const expenses = copyArray(data.expenses) || [];
  
    if(index == -1) {
      expenses.push({qty: 1});
    }else{
      expenses.splice(index+1, 0, {qty: 1});
    }
  
    store.setState({data: {...data, expenses}});
  }

  const updateExpense = (index, expenseData) => {
    for(let [k,v] of Object.entries(expenseData)) {
      if(k.endsWith('_obj')) expenseData[k.replace('_obj', '')] = v?.id;
    }
    
    const {data} = store.getState();
    const expenses = copyArray(data.expenses) || [];
    expenses[index] = {...expenses[index], ...expenseData};
    store.setState({data: {...data, expenses}});
  }

  const deleteExpense = (index) => {
    const {data} = store.getState();
    const expenses = copyArray(data.expenses) || [];
    expenses.splice(index, 1);
    store.setState({data: {...data, expenses}});
  }

  let ncol = 4;
  if(readOnly) ncol -= 1;
  
  return(
    <div style={{overflow: "auto", minHeight: "200px"}}>
      <table className="table mt-3">
        <thead>
          <tr>
            {!readOnly &&
              <th className="text-center">
                <a className="ms-3" href='#/' onClick={() => addExpense(-1)}>
                  <i className="fas fa-plus"></i>
                </a>
              </th>
            }
            <th style={{width: '30%'}}>
              Loại chi phí
            </th>
            <th style={{width: '25%'}}>
              Số tiền
            </th>
            <th style={{width: '40%'}}>
              Ghi chú
            </th>
          </tr>
        </thead>
        <tbody>
          {expenses.length === 0 &&
            <tr>
              <td colSpan={ncol}>
                Chưa có chi phí
              </td>
            </tr>
          }
          {expenses.map((expense, index) => 
            <tr key={index}>
              {!readOnly &&
                <td>
                  <>
                    <a className="me-2" href='#/' onClick={() => deleteExpense(index)}>
                      <i className="fas fa-trash text-danger"></i>
                    </a>
                    <a href='#/' onClick={() => addExpense(index)}>
                      <i className="fas fa-plus"></i>
                    </a>
                  </>
                </td>
              }

              <td>
                <Input
                  type="async-select"
                  readOnly={readOnly}
                  value={expense.type_obj}
                  onChange={val => updateExpense(index, {type_obj: val})}
                  optionsUrl="/sales/search-expense-type"
                  labelField="name"
                />
                <ErrorList errors={errors?.expenses?.[index]?.type}/>
              </td>

             
              <td>
                <Input
                  type="number"
                  readOnly={readOnly}
                  value={expense.amount}
                  onChange={val => updateExpense(index, {amount: val})}
                  min="0"
                />
                <ErrorList errors={errors?.expenses?.[index]?.amount}/>
              </td>
              
              <td>
                <Input
                  type="input"
                  readOnly={readOnly}
                  value={expense.note}
                  onChange={val => updateExpense(index, {note: val})}
                  min="1"
                />
                <ErrorList errors={errors?.expenses?.[index]?.note}/>
              </td>
             
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}