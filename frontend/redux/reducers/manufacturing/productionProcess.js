import formReducer from './productionProcess/formReducer';
import {combineReducers} from 'redux';

const reducer = combineReducers({
  form: formReducer
});

export default reducer;