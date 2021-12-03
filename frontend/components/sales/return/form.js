import axios from 'axios';
import { useEffect } from 'react';
import { useRouter } from 'next/router';

import { Tab, Tabs } from 'react-bootstrap';
import Card from 'components/share/card';
import Input from "components/share/input";
import ErrorList from "components/share/errorlist";

import DebtDeductNote from '../sections/note/debtDeductNote';
import PaymentNote from '../sections/note/paymentNote';
import InStockNote from '../sections/note/inStockNote';
import Invoice from '../sections/note/invoice';

import GoodItems from '../sections/itemList/goodsItems';

import { 
  IconLink, 
  IconButton, 
  useSliceStore, 
  useSliceSelector,
  Spiner
} from 'utils/helper';

import { NAME_SPACE } from 'redux/reducers/sales/formReducer';


const itemName = 'yêu cầu trả lại hàng bán';

export default function ReturnForm({id, update, readOnly}){
  const baseUrl = '/sales/order/crud';
  const backUrl = (update || readOnly)? '../' : '../return';
  const editUrl = id? `../update/${id}` : null;
  
  const router = useRouter();
  const store = useSliceStore(NAME_SPACE);
  const [data, errors] = useSliceSelector(NAME_SPACE, ['data', 'errors']);

  useEffect(() => {
    store.setState({
      data: {},
      errors: {}
    });

    if(id) {
      axios.get(`${baseUrl}/${id}`).then(result => {
        store.setState({data: result.data});
      });
    }
  }, [id]);

  const updateData = newData => {
    for(let [k,v] of Object.entries(newData)) {
      if(k.endsWith('_obj')) newData[k.replace('_obj', '')] = v?.id;
    }

    const data = store.getState().data ?? {};
    
    store.setState({
      data: {
        ...data,
        ...newData
      }
    }) 
  }
  
  const saveReturn = async (e) => {
    e.preventDefault();
    if(readOnly) return; 

    const {data} = store.getState();
    data.type = 'RETURN';

    data?.items?.forEach(item => {
      item.amount_tax = item.discount = 0;
    });

    try{
      await axios.post(`${baseUrl}/`, data);
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
  
  const loading = (update || readOnly) && !data.id;
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
        <form id="fmt" onSubmit={saveReturn}>
          <div className="row">
            <div className="col p-2">
              <div className="section-title">Thông tin khách hàng</div>
              <hr className="mt-0"/>
              <table className="table">
                <tbody>
                  <tr>
                    <th style={{width: '25%'}}>Khách hàng:</th>
                    <td>
                      <Input
                        type="async-select"
                        readOnly={readOnly}
                        value={data.customer_obj}
                        onChange={(val) => updateData({customer_obj: val})}
                        optionsUrl="/sales/search-customer"
                        labelField="name"
                      />
                      <ErrorList errors={errors.customer}/>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div className="row">
            <div className="col p-2">
              <div className="section-title">Thông tin chung</div>
              <hr className="my-0"/>
            </div>
          </div>

          <Tabs className="mt-2">
            <Tab eventKey="debtDeductNote" title="Chứng từ giảm công nợ">
              <DebtDeductNote readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="paymentNote" title="Phiếu chi">
              <PaymentNote readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="inStockNote" title="Phiếu nhập">
              <InStockNote readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="invoice" title="Hoá đơn">
              <Invoice readOnly={readOnly} invoiceReadOnly={true}/>
            </Tab>
          </Tabs>

          <div className="row mt-3">
            <div className="col p-2">
              <div className="section-title">Thông tin hàng hoá/dịch vụ</div>
              <hr className="my-0"/>
            </div>
          </div>
          
          <GoodItems 
            readOnly={readOnly}
            withImport={true}
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