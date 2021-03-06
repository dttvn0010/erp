import axios from 'axios';
import { useEffect } from 'react';
import { useRouter } from 'next/router';

import { Tab, Tabs } from 'react-bootstrap';
import Card from 'components/share/card';
import Input from "components/share/input";
import ErrorList from "components/share/errorlist";

import ReceiptNote from '../sections/note/receiptNote';
import DebtDeductNote from '../sections/note/debtDeductNote';
import Invoice from '../sections/note/invoice';

import GoodItems from '../sections/itemList/goodsItems';

import { 
  IconLink, 
  IconButton, 
  useSliceStore, 
  useSliceSelector,
  Spiner
} from 'utils/helper';

import { NAME_SPACE } from 'redux/reducers/purchase/formReducer';

const itemName = 'yêu cầu giảm giá hàng mua';

export default function DiscountForm({id, update, readOnly}){
  const baseUrl = '/purchase/order/crud';
  const backUrl = (update || readOnly)? '../' : '../discount';
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

  const saveDiscount = async (e) => {
    e.preventDefault();
    if(readOnly) return; 

    const {data} = store.getState();
    data.type = 'DISCOUNT';

    //console.log('data=', data);

    data?.items?.forEach(item => {
      item.amount_tax = item.discount = 0;
    });
  
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
        <form id="fmt" onSubmit={saveDiscount}>
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
            <Tab eventKey="debtDeductNote" title="Chứng từ giảm công nợ">
              <DebtDeductNote readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="receiptNote" title="Phiếu thu">
              <ReceiptNote readOnly={readOnly}/>
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
          
          <GoodItems readOnly={readOnly}/>

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