import indexReducer from './account/indexReducer';
import {combineReducers} from 'redux';

const reducer = combineReducers({
    index: indexReducer
});

export default reducer;