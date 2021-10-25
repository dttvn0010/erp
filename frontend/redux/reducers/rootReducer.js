import counterReducer from './counterReducer';
import appReducer from './appReducer';
import purchaseReducer from './purchase';
import salesReducer from './sales';
import accountingReducer from './accounting';

import {combineReducers} from 'redux';

const rootReducer = combineReducers({
    app: appReducer,
    counter: counterReducer,
    purchase: purchaseReducer,
    sales: salesReducer,
    accounting: accountingReducer
});

export default rootReducer;