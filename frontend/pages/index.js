import {  useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import DatePicker from "react-datepicker";
import Select from 'react-select'

import Layout from '../components/share/layout'
import DataTable from '../components/share/datatable';

import {incrementCounter} from '../redux/actions/counterActions';
import { copyArray } from 'utils/helper';
import { createForm } from 'components/share/form';

const formMeta= {
  fields: [
    {
      name: 'bank',
      label: 'Ngân hàng',
      type: 'select',
      attrs: {
        optionsUrl: '/accounting/bank-account/search-bank',
        labelField: 'name'
      }
    },
    {
      name: 'bank_account',
      keys: ['bank'],
      label: 'Tài khoản ngân hàng',
      type: 'select',
      attrs: {
        optionsUrl: '/accounting/search-bank-account',
        getParams: (id, data) => ({bank_id: data?.bank}),
        labelField: 'name'
      }
    }
  ]
}

export default function Index() {
  const dispatch = useDispatch();
  const count = useSelector(state => state.counter.value);
  const [startDate, setStartDate] = useState(new Date());  

  const [form, setForm] = useState(null);

  useEffect(() => {
    setForm(createForm(formMeta));
  }, []);

  const saveForm = (e) => {
    e.preventDefault();
    //const data = new FormData(document.getElementById("fmt"));
    
  }
  
  const options = [
    { value: 'chocolate', label: 'Chocolate' },
    { value: 'strawberry', label: 'Strawberry' },
    { value: 'vanilla', label: 'Vanilla' }
  ];

  const [drink, setDrink] = useState("");

  const [items, setItems] = useState([{}]);

  const addItem = (index) => {
    const items1 = copyArray(items) || [];
    console.log('items==', items1);
    if(index == -1) {
      items1.push({});
    }else{
      items1.splice(index+1, 0, {});
    }

    console.log('index=', index, 'items=', items1);

    setItems(items1);
  }

  const updateItem = (index, itemData) => {
    const items1 = copyArray(items) || [];
    items1[index] = {...items1[index], ...itemData};
    setItems(items1);
  }

  /*
  const customers = [
    {
      id: 1,
      name: 'Customer 1',
      phone: '123456789',
      email: 'customer1@gmail.com',
      address: 'No.1, Street 1, City 1'
    },
    {
      id: 2,
      name: 'Customer 2',
      phone: '123456780',
      email: 'customer2@gmail.com',
      address: 'No.2, Street 2, City 2'
    },
    {
      id: 3,
      name: 'Customer 3',
      phone: '123456781',
      email: 'customer3@gmail.com',
      address: 'No.3, Street 3, City 3'
    },
    {
      id: 4,
      name: 'Customer 4',
      phone: '123456783',
      email: 'customer4@gmail.com',
      address: 'No.4, Street 4, City 4'
    },
    {
      id: 5,
      name: 'Customer 5',
      phone: '123456790',
      email: 'customer5@gmail.com',
      address: 'No.5, Street 5, City 5'
    }
  ];

  const columnsDef = [
    {
      name: 'name',
      title: 'Name',
      searchable: true,
      orderable: true,
      editable: true
    },
    {
      name: 'phone',
      title: 'Phone',
      searchable: true,
      orderable: true,
      editable: true
    },
    {
      name: 'email',
      title: 'Email',
      searchable: true,
      orderable: true,
      editable: true
    },
    {
      name: 'address',
      title: 'Address',
      searchable: true,
      orderable: true,
      editable: true
    }
  ];*/

  return (
    <div className="container mt-3">
      <h2>Home</h2>
      {form && <form.All headerWidth={"30%"}/>}
      <div>Counter: {count}</div>
      
      <button 
        className="btn btn-primary btn-sm"
        onClick={() => dispatch(incrementCounter())}
      >
        Click
      </button>
      
      {items.map((item, index) =>
        <div>
          <button className="btn btn-sm btn-primary" onClick={() => addItem(index)}>Add</button>
          <input name={`inp_${index}`} defaultValue={index}/>
        </div>
      )}
      <DataTable apiUrl={"/stock/product-category/search"}/>

      <form onSubmit={saveForm} id="fmt">
        <div className="row">
          <div className="col-3">
            <DatePicker
              className="form-control"
              name="startDate"
              selected={startDate}
              onChange={(date) => setStartDate(date)}
              timeInputLabel="Time:"
              dateFormat="dd/MM/yyyy HH:mm"
              showTimeInput
            />
          </div>
          <div className="col-3">
            <Select 
              isMulti={true}
              name="drink"
              value={drink}
              onChange={(value) => setDrink(value)}
              options={options} 
              isClearable={true}
              placeholder="Chọn loại kem"
            />
          </div>
        </div>
        <div className="row mt-3">
          <div className="col">
            <button type="submit" className="btn btn-sm btn-primary">Hello</button>
          </div>
        </div>
      </form>
    </div>
  )
}

Index.getLayout = function getLayout(page) {
  return (
    <Layout>
      {page}
    </Layout>
  )
}