import {combineReducers} from 'redux';
import accountReducer from './account_reducer';

const reducer = combineReducers({
    account: accountReducer,
});

export default reducer;