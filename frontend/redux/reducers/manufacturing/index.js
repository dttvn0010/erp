import productBomReducer from './productBomReducer';
import productionWorkflowReducer from './productionWorkflow';
import productionProcessReducer from './productionProcess';
import {combineReducers} from 'redux';

const reducer = combineReducers({
  productBom: productBomReducer,
  productionWorkflow: productionWorkflowReducer,
  productionProcess: productionProcessReducer
});

export default reducer;