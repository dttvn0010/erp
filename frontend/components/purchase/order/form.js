import axios from 'axios';
import { useEffect } from 'react';
import { useRouter } from 'next/router';

import Card from 'components/share/card';
import Input from 'components/share/input';
import ErrorList from 'components/share/errorlist';

import { 
  IconLink, 
  IconButton, 
  useSliceStore, 
  useSliceSelector,
  copyArray,
  Spiner
} from 'utils/helper';

import { NAME_SPACE } from 'redux/reducers/purchase/order/formReducer';

const itemName = 'đơn mua hàng';

const addOrderLine = (store, index) => {
  let {order_lines} = store.getState();
  order_lines = copyArray(order_lines);

  if(index == -1) {
    order_lines.push({qty: 1});
  }else{
    order_lines.splice(index+1, 0, {qty: 1});
  }

  store.setState({order_lines});
}

function OrderLineTable({readOnly}) {
  const store = useSliceStore(NAME_SPACE);
  const [order_lines, errors] = useSliceSelector(NAME_SPACE, ['order_lines', 'errors']);

  const updateOrderLine = (index, data) => {
    let {order_lines} = store.getState();
    order_lines = copyArray(order_lines);
    order_lines[index] = {...order_lines[index], ...data};
    store.setState({order_lines});
  }

  const deleteOrderLine = (index) => {
    let {order_lines} = store.getState();
    order_lines = copyArray(order_lines);
    order_lines.splice(index, 1);
    store.setState({order_lines});
  }
  
  return(
    <>
      <div className="row">
        <div className="col">
          <h5>Chi tiết các mặt hàng</h5>
          {!readOnly &&
            <div className="float-end">
              <button type="button" 
                className="btn btn-sm btn-primary mb-2" 
                onClick={() => addOrderLine(store, -1)}
              >
                <i className="fas fa-plus"></i> Thêm mặt hàng
              </button>
            </div>
          }
        </div>
      </div>

      <table className="table" style={{width: "100%"}}>
        <thead>
          <tr>
            <th></th>
            <th style={{width: "35%"}}>Tên mặt hàng</th>
            <th style={{width: "20%"}} className="text-center">Đơn giá</th>
            <th style={{width: "20%"}} className="text-center">Số lượng</th>
            <th style={{width: "20%"}} className="text-center">Thành tiền</th>
          </tr>
        </thead>
        <tbody>
          {order_lines.length === 0 &&
            <tr>
              <td colSpan="5">
                Chưa có mặt hàng nào
              </td>
            </tr>
          }
          {order_lines.map((order_line, index) => 
            <tr key={index}>
              <td className="text-center">
                <a className="me-2" href='#/' onClick={() => deleteOrderLine(index)}>
                  <i className="fas fa-trash text-danger"></i>
                </a>

                <a href='#/' onClick={() => addOrderLine(store, index)}>
                  <i className="fas fa-plus"></i>
                </a>
              </td>

              <td>
                <Input
                  type="async-select"
                  readOnly={readOnly}
                  value={{
                    value: order_line.product,
                    label: order_line.product_name
                  }}
                  onChange={(data) => updateOrderLine(index, {
                    product: data?.value,
                    product_name: data?.label,
                    price_unit: data?.price_unit
                  })}
                  optionsUrl="/purchase/order/search-product"
                  labelField="name"
                />
                <ErrorList errors={errors[`order_lines[${index}]`]?.product}/>
              </td>

              <td className="text-center">
                <Input
                  type="number"
                  readOnly={readOnly}
                  value={order_line.price_unit}
                  onChange={
                    val => updateOrderLine(index, {price_unit: val})
                  }
                  className="text-center"
                  min="0"
                  step="1000"
                />
                <ErrorList errors={errors[`order_lines[${index}]`]?.price_unit}/>
              </td>

              <td className="text-center">
                <Input
                  type="number"
                  readOnly={readOnly}
                  value={order_line.qty}
                  onChange={
                    val => updateOrderLine(index, {qty: val})
                  }
                  className="text-center"
                  min="1"
                />
                <ErrorList errors={errors[`order_lines[${index}]`]?.qty}/>
              </td>

              <td className="text-center">
                {order_line.qty && order_line.price_unit &&
                  <span>{order_line.qty * order_line.price_unit} đ</span>
                }
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </>
  )
}

export default function OrderForm({id, update, readOnly}){
  const baseUrl = '/purchase/order/api';
  const backUrl = (update || readOnly)? '../' : '../order';
  const editUrl = id? `../update/${id}` : null;
  
  const router = useRouter();
  const store = useSliceStore(NAME_SPACE);
  const [order, errors] = useSliceSelector(NAME_SPACE, ['order', 'errors']);

  useEffect(() => {
    store.setState({
      order: {},
      order_lines: [],
      errors: {}
    });

    if(id) {
      axios.get(`${baseUrl}/detail/${id}`).then(result => {
        const {order_lines, ...order} = result.data;
        store.setState({
          order,
          order_lines
        });
      });
    }
  }, [id]);

  const saveOrder = async (e) => {
    e.preventDefault();
    if(readOnly) return; 

    const {order, order_lines} = store.getState();

    const data = {
      ...order,
      order_lines
    };

    try{
      await axios.post(`${baseUrl}/save`, data);
      router.push(backUrl);
    }catch(err){
      store.setState({
        errors: err?.response?.data ?? {}
      });
      alert('Đã có lỗi xảy ra');
    }
  }

  const title = (
    readOnly? `Xem ${itemName}` : (update? `Cập nhập ${itemName}` : `Tạo mới ${itemName}`)
  );

  const updateOrder = (data) => {
    store.setState({
      order: {...order, ...data}
    });
  }
  
  const loading = (update || readOnly) && !order.id;
  if(loading) {
    return(
      <div className="text-center p-3">
        <Spiner/>
      </div>
    )
  }

  return (
    <Card
      title={title}
      body={
        <form id="fmt" onSubmit={saveOrder}>
          <div className="row">
            <div className="col">
              <table className="table">
                <tbody>
                  <tr>
                    <th>Nhà cung cấp*:</th>
                    <td>
                      <Input
                        type="async-select"
                        readOnly={readOnly}
                        value={{
                          value: order.supplier,
                          label: order.supplier_name
                        }}
                        onChange={
                          data => updateOrder({
                            supplier: data?.value, 
                            supplier_name: data?.label
                          })
                        }
                        optionsUrl="/purchase/order/search-supplier"
                        labelField="name"
                      />
                      <ErrorList errors={errors.supplier}/>
                    </td>
                  </tr>
                  <tr>
                    <th>Ghi chú:</th>
                    <td>
                      <Input
                        type="textarea"
                        readOnly={readOnly}
                        value={order.note}
                        onChange={val => updateOrder({note: val})}
                        rows="5"
                      />
                      <ErrorList errors={errors.note}/>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <OrderLineTable
            readOnly={readOnly}
          />

          <div className="row mt-3">
            <div className="col">
              <div>
                <IconLink 
                  href={backUrl}
                  icon="arrow-left"
                  variant="secondary"
                  title="Quay lại"
                  className="me-2"
                />
                {!readOnly &&
                  <IconButton
                    icon="save"
                    type="submit"
                    title="Lưu lại"
                  />
                }
                {readOnly && 
                  <IconLink
                    href={editUrl}
                    icon="edit"
                    title="Cập nhật"
                  />
                }
              </div>
            </div>
          </div>
        </form>
      }
    />
  )
}