import formReducer from './discount/formReducer';
import {combineReducers} from 'redux';

const reducer = combineReducers({
    form: formReducer
});

export default reducer;