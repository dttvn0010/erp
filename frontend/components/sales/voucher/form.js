import axios from 'axios';
import { useEffect } from 'react';
import { useRouter } from 'next/router';

import { Tab, Tabs } from 'react-bootstrap';
import Card from 'components/share/card';
import Input from "components/share/input";
import ErrorList from "components/share/errorlist";

import DebtNote from '../sections/note/debtNote';
import OutStockNote from '../sections/note/outStockNote';
import ReceiptNote from '../sections/note/receiptNote';
import DepositNote from '../sections/note/depositNote';
import Invoice from '../sections/note/invoice';

import GoodItems from '../sections/itemList/goodsItems';
import ExpenseList from '../sections/itemList/expenseList';

import { 
  IconLink, 
  IconButton, 
  useSliceStore, 
  useSliceSelector,
  Spiner
} from 'utils/helper';

import { NAME_SPACE } from 'redux/reducers/sales/voucher/formReducer';


const itemName = 'chứng từ bán hàng';

export default function VoucherForm({id, update, readOnly}){
  const baseUrl = '/sales/voucher/api';
  const backUrl = (update || readOnly)? '../' : '../voucher';
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
      axios.get(`${baseUrl}/detail/${id}`).then(result => {
        store.setState({data: result.data});
      });
    }
  }, [id]);

  const updateData = newData => {
    const data = store.getState().data ?? {};
    
    store.setState({
      data: {
        ...data,
        ...newData
      }
    }) 
  }

  const saveVoucher = async (e) => {
    e.preventDefault();
    if(readOnly) return; 

    const {data} = store.getState();

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
        <form id="fmt" onSubmit={saveVoucher}>
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
                        value={data.customer}
                        onChange={(val) => updateData({customer: val})}
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
              <div className="section-title">Thông tin chứng từ</div>
              <hr className="my-0"/>
            </div>
          </div>

          <Tabs className="mt-2">
            <Tab eventKey="debtNote" title="Chứng từ ghi nợ">
              <DebtNote readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="receiptNote" title="Phiếu thu">
              <ReceiptNote readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="depositNote" title="Thu tiền gửi">
              <DepositNote readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="outStockNote" title="Phiếu xuất">
              <OutStockNote readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="invoice" title="Hoá đơn">
              <Invoice readOnly={readOnly}/>
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
            withTax={true}
            withStock={true}
            withDiscount={true}
          />

          <div className="row mt-2">
            <div className="col p-2">
              <div className="section-title">Chi phí bán hàng kèm theo</div>
              <hr className="my-0"/>
            </div>
          </div>

          <ExpenseList readOnly={readOnly}/>

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