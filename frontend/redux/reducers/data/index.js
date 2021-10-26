import {combineReducers} from 'redux';
import accountingReducer from './accounting';

const reducer = combineReducers({
    accounting: accountingReducer,
});

export default reducer;