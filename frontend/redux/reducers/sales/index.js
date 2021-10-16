import voucherReducer from './voucherReducer';
import discountReducer from './discountReducer';
import returnReducer from './returnReducer';
import {combineReducers} from 'redux';

const reducer = combineReducers({
    voucher: voucherReducer,
    discount: discountReducer,
    return: returnReducer
});

export default reducer;