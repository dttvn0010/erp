import counterReducer from './counterReducer';
import appReducer from './appReducer';
import purchaseReducer from './purchase/purchaseReducer';

import {combineReducers} from 'redux';

const rootReducer = combineReducers({
    app: appReducer,
    counter: counterReducer,
    purchase: purchaseReducer
});

export default rootReducer;