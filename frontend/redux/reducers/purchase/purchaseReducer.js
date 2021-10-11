import orderReducer from './orderReducer';
import {combineReducers} from 'redux';

const reducer = combineReducers({
    order: orderReducer
});

export default reducer;