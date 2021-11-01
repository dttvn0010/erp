import counterReducer from './counterReducer';
import appReducer from './appReducer';
import purchaseReducer from './purchase';
import salesReducer from './sales';
import accountingReducer from './accounting';
import stockReducer from './stock';
import manufacturingReducer from './manufacturing';
import dataReducer from './data';

import {combineReducers} from 'redux';

const rootReducer = combineReducers({
    app: appReducer,
    counter: counterReducer,
    purchase: purchaseReducer,
    sales: salesReducer,
    accounting: accountingReducer,
    stock: stockReducer,
    manufacturing: manufacturingReducer,
    data: dataReducer
});

export default rootReducer;