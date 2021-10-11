export const Action = {
  SET_STATE: 'setState'
}

const initialState = {
  selectedPage: null
}

const reducer = (state=initialState, action) => {
  if(action.type === 'app/' + Action.SET_STATE) {
    return {...state, ...action.payload};
  }
  return state;
}

export default reducer;