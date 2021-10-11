import {  useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import DatePicker from "react-datepicker";
import Select from 'react-select'

import Layout from '../components/share/layout'
import DataTable from '../components/share/datatable';

import {incrementCounter} from '../redux/actions/counterActions';

export default function Index() {
  const dispatch = useDispatch();
  const count = useSelector(state => state.counter.value);
  const [startDate, setStartDate] = useState(new Date());  
  const saveForm = (e) => {
    e.preventDefault();
    const data = new FormData(document.getElementById("fmt"));
    console.log(data.get("startDate"), data.get("drink"));
  }
  
  const options = [
    { value: 'chocolate', label: 'Chocolate' },
    { value: 'strawberry', label: 'Strawberry' },
    { value: 'vanilla', label: 'Vanilla' }
  ];

  const [drink, setDrink] = useState("");

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
      <div>Counter: {count}</div>
      
      <button 
        className="btn btn-primary btn-sm"
        onClick={() => dispatch(incrementCounter())}
      >
        Click
      </button>
      
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