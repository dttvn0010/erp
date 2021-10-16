import counterReducer from './counterReducer';
import appReducer from './appReducer';
import purchaseReducer from './purchase';
import salesReducer from './sales';

import {combineReducers} from 'redux';

const rootReducer = combineReducers({
    app: appReducer,
    counter: counterReducer,
    purchase: purchaseReducer,
    sales: salesReducer
});

export default rootReducer;