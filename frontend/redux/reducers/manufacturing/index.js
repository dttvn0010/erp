import productBomReducer from './productBomReducer';
import {combineReducers} from 'redux';

const reducer = combineReducers({
  productBom: productBomReducer,
});

export default reducer;