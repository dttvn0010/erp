export const NAME_SPACE = 'stock/export/form';

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