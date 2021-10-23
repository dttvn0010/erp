import axios from "axios";
import Link from 'next/link';
import { useSelector } from "react-redux";
import { useStore } from "react-redux";
import Layout from 'components/share/layout';

function stateEqual(state1, state2) {
  for(let key in state1) {
    if(state1[key] != state2[key]) {
      return false;
    }
  }
  return true;
}

export function useMapSelector(mapFunc) {
  return useSelector(mapFunc, stateEqual);
}

export function useSliceSelector(namespace, keys) {
  let preKeys = namespace.split('/');
  return useMapSelector(globalState => {
      let pageStates = globalState;
      preKeys.forEach(preKey => pageStates = pageStates[preKey] || {});
      let selectedStates = [];
      keys.forEach(key => selectedStates.push(pageStates[key]));
      return selectedStates;
    }
  );
}

class SliceStore {
  constructor(namespace, store) {
    this._namespace = namespace;
    this._store = store;
  }

  dispatch(action) {
    this._store.dispatch({
      type: `${this._namespace}/${action.type}`, 
      payload: action.payload
    });
  }

  dispatchGlobal(action) {
    this._store.dispatch(action);
  }

  setState(payload) {
    this._store.dispatch({
      type: `${this._namespace}/setState`, 
      payload: payload
    });
  }

  getState() {
    let keys = this._namespace.split('/');
    let state = this._store.getState();
    keys.forEach(key => state = state[key] || {});
    return state; 
  }

  getGlobalState() {
    return this._store.getState();
  }
}

export function useSliceStore(namespace) {
  let store = useStore();
  return new SliceStore(namespace, store);
}

function appendUrlParams(url, params) {
  if(!url.includes('?')) url += '?';
  for(let [key,value] of Object.entries(params)) {
    if(value){
      url += `&${key}=${encodeURIComponent(value)}`;
    }
  }
  return url;
}

export async function getOptions({url, params, labelField, labelDiplayFunc, valueField}) {
  let result = await axios.get(appendUrlParams(url, params));
  let options = [{
    label: '---------',
    value: ''
  }];

  (result?.data??[]).forEach(item => options.push({
    ...item,
    label: labelDiplayFunc? labelDiplayFunc(item) : item[labelField], 
    value: item[valueField]
  }));

  return options;
}

export function getLoadOptions({url, params, getParams, labelField, labelDiplayFunc, valueField}) {
  return (term, callback) => {
    params = params || {};
    
    if(getParams) {
      params = {...params, ...getParams()};
    }
    
    axios.get(appendUrlParams(url, {...params, term})).then(result => {
      let options = (result.data??[]).map(item => ({
        ...item,
        label: (labelDiplayFunc? labelDiplayFunc(item): item[labelField]), 
        value: item[valueField]
      }));
      
      if(options.length >= 30) {
        options.push({
          label: 'Gõ vào để tìm kiếm ...',
          value: '',
          isDisabled: true
        });
      }

      callback(options);
    });
  }
}

export function getDeleteItemHandler(itemName, url) {
  return (dispatch, row) => {
    if(!confirm(`Bạn có chắc muốn xóa ${itemName} này không?`)){
      return;
    }
    axios.delete(url.replace('[$id$]', row.pk)).then(() => {
      dispatch.reload();
    }).catch(() => {
      alert(`Xóa ${itemName} không thành công`);
    });
  }
}

export function getChangeStatusItemHandler(itemName, url) {
  return (dispatch, row) => {
    if(!confirm(`Bạn có chắc muốn đổi trạng thái ${itemName} này?`)){
      return;
    }
    axios.post(url.replace('[$id$]', row.pk)).then(() => {
      dispatch.reload();
    }).catch(() => {
      alert("Đổi trạng thái không thành công");
    });
  }
}

export function getStatusSwitcher(data, row, dispatch, itemName, changeStatusUrl) {
  const changeItemStatus = getChangeStatusItemHandler(itemName, changeStatusUrl);
  return(
    <div className="d-flex">
      <div className="px-1" style={{flex: 1}}>
        {data}
      </div>

      <div className="px-0 text-center">
        <div className="form-check form-switch">
          <input 
            type="checkbox" 
            className="form-check-input"
            checked={row.status_id === 'ACTIVE'}
            onChange={() => changeItemStatus(dispatch, row)}
          />
        </div>
      </div>
    </div>
  )
}

export function IconLink({title, icon, href, variant, size, className}) {
  return (
    <Link href={href ?? '#/'}>
      <a 
        className={`btn btn-${size ?? 'sm'} btn-${variant ?? 'primary'} ${className ?? ''}`}
      >
        <i className={`fas fa-${icon ?? ''} text-white-50`}></i> {title}
      </a>
    </Link>
  );
}

export function IconButton({title, icon, variant, size, className, type}) {
  return (
    <button 
      type={type} 
      className={`btn btn-${size ?? 'sm'} btn-${variant ?? 'primary'} ${className ?? ''}`}
    >
      <i className={`fas fa-${icon ?? ''} text-white-50`}></i> {title}
    </button>
  );
}

export function Spiner() {
  return(
    <div className="spinner-border" role="status">
      <span className="sr-only"></span>
    </div>
  );
}

export const getDefaultLayOut = (page) => {
  return (
    <Layout>
      {page}
    </Layout>
  )
}

export function serializeForm(fmt) {
  let formData = new FormData(fmt);
  let data = {};
  for(let pair of formData.entries()) {
    data[pair[0]] = pair[1]
  }
  return data;
}

export function copyObject(obj) {
  return {...obj};
}

export function copyArray(arr) {
  if(Array.isArray(arr)){
    return [...arr];
  }
}