import importReducer from './importReducer';
import exportReducer from './exportReducer';
import exchangeReducer from './exchangeReducer';
import inventoryReducer from './inventoryReducer';
import {combineReducers} from 'redux';

const reducer = combineReducers({
    import: importReducer,
    export: exportReducer,
    exchange: exchangeReducer,
    inventory: inventoryReducer,
});

export default reducer;