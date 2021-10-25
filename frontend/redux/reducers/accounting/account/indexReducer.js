export const NAME_SPACE = 'accounting/account/index';

export const ACTIONS = {
  SET_STATE: 'setState'
}
  
const initialState = {
  showBalanceModal: false,
  accountId: null,
  accountNumber: '',
  balance: null
}

const reducer = (state=initialState, action) => {
  if(action.type === NAME_SPACE + '/' + ACTIONS.SET_STATE) {
    return {...state, ...action.payload};
  }
  return state;
}

export default reducer;