import axios from 'axios';
import { useEffect } from 'react';
import { useRouter } from 'next/router';

import { Tab, Tabs } from 'react-bootstrap';
import Card from 'components/share/card';
import Input from "components/share/input";
import ErrorList from "components/share/errorlist";

import InStockNote from '../sections/note/inStockNote';
import PaymentNote from '../sections/note/paymentNote';
import WithdrawNote from '../sections/note/withdrawNote';
import DebtNote from '../sections/note/debtNote';
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

import { NAME_SPACE } from 'redux/reducers/purchase/formReducer';

const itemName = 'đơn mua hàng';

export default function VoucherForm({id, update, readOnly}){
  const baseUrl = '/purchase/order/crud';
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

  const saveVoucher = async (e) => {
    e.preventDefault();
    if(readOnly) return; 

    const {data} = store.getState();
    data.type = 'PURCHASE';
  
    data?.items?.forEach(item => {
      if(item.price_unit && item.qty){
        const total = item.price_unit * item.qty;
        if(item.amount_tax_pctg) {
          item.amount_tax = Math.round(total * item.amount_tax_pctg/100)
        }
        if(item.discount_pctg) {
          item.discount = Math.round(total * item.discount_pctg/100)
        }
      }
    });

    //console.log('data=', data);
  
    try{
      await axios.post(`${baseUrl}/`, data);
      router.push(backUrl);
    }catch(err){
      //console.log('err=', err?.response?.data);
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
              <div className="section-title">Thông tin nhà cung cấp</div>
              <hr className="mt-0"/>
              <table className="table">
                <tbody>
                  <tr>
                    <th style={{width: '25%'}}>Nhà cung cấp:</th>
                    <td>
                      <Input
                        type="async-select"
                        readOnly={readOnly}
                        value={data.supplier_obj}
                        onChange={(val) => updateData({supplier_obj: val})}
                        optionsUrl="/purchase/search-supplier"
                        labelField="name"
                      />
                      <ErrorList errors={errors.supplier}/>
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
            <Tab eventKey="debtNote" title="Chứng từ ghi nợ">
              <DebtNote readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="paymentNote" title="Phiếu chi">
              <PaymentNote readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="withdrawNote" title="Phiếu chuyển khoản">
              <WithdrawNote readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="inStockNote" title="Phiếu nhập">
              <InStockNote readOnly={readOnly}/>
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
            withImport={true}
            withTax={true}
            withDiscount={true}
          />

          <div className="row mt-2">
            <div className="col p-2">
              <div className="section-title">Chi phí mua hàng kèm theo</div>
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
                {readOnly && false &&
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