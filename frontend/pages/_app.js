import {Provider} from 'react-redux';
import axios from 'axios';
import store from '../redux/store';

import '../styles/globals.css'
import '../styles/sb-admin2.css'
import '../styles/font-awesome/css/all.css'
import "../styles/react-datepicker.css"
import "../styles/datatable.css"
import '../styles/login.css'

axios.defaults.baseURL = 'http://127.0.0.1:8000';
axios.defaults.headers.post['Content-Type'] = 'application/json';

axios.interceptors.request.use(request => {
  request.headers.common.Authorization = 'Bearer ' + localStorage.getItem('token');
  return request;
});

axios.interceptors.response.use(response => {
  return response
}, err => {
  if(err?.response?.status === 403) {
    localStorage.removeItem('token');
    location.href = '/login';
  }
  return Promise.reject(err);
});

function MyApp({ Component, pageProps }) {
  const getLayout = Component.getLayout || ((page) => page);
  return (
    <Provider store={store}>
      {getLayout(<Component {...pageProps} />)}
    </Provider>
  )
}

export default MyApp;
