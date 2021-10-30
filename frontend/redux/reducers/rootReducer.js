import counterReducer from './counterReducer';
import appReducer from './appReducer';
import purchaseReducer from './purchase';
import salesReducer from './sales';
import accountingReducer from './accounting';
import stockReducer from './stock';
import dataReducer from './data';

import {combineReducers} from 'redux';

const rootReducer = combineReducers({
    app: appReducer,
    counter: counterReducer,
    purchase: purchaseReducer,
    sales: salesReducer,
    accounting: accountingReducer,
    stock: stockReducer,
    data: dataReducer
});

export default rootReducer;