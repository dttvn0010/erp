import expenseReducer from './expenseReducer';
import incomeReducer from './incomeReducer';
import internalTransferReducer from './internalTransferReducer';
import {combineReducers} from 'redux';

const reducer = combineReducers({
    expense: expenseReducer,
    income: incomeReducer,
    internalTransfer: internalTransferReducer
});

export default reducer;