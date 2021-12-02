import formReducer from './formReducer';
import {combineReducers} from 'redux';

const reducer = combineReducers({
    form: formReducer,
});

export default reducer;