export const NAME_SPACE = 'accounting/expense/form';

export const ACTIONS = {
  SET_STATE: 'setState'
}
  
const initialState = {
  data: {},
  errors: {},
}

const reducer = (state=initialState, action) => {
  if(action.type === NAME_SPACE + '/' + ACTIONS.SET_STATE) {
    return {...state, ...action.payload};
  }
  return state;
}

export default reducer;