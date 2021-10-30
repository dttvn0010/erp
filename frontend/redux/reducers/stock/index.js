import importReducer from './importReducer';
import exportReducer from './exportReducer';
import exchangeReducer from './exchangeReducer';
import {combineReducers} from 'redux';

const reducer = combineReducers({
    import: importReducer,
    export: exportReducer,
    exchange: exchangeReducer
});

export default reducer;