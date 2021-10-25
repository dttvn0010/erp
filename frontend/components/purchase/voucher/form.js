import axios from 'axios';
import { useEffect } from 'react';
import { useRouter } from 'next/router';

import { Tab, Tabs } from 'react-bootstrap';
import Card from 'components/share/card';
import InStockNote from '../sections/note/inStockNote';
import PaymentNote from '../sections/note/paymentNote';
import WithdrawNote from '../sections/note/withdrawNote';
import DebtNote from '../sections/note/debtNote';
import Invoice from '../sections/note/invoice';

import GoodItems from '../sections/item_list/goodsItems';
import TaxItems from '../sections/item_list/taxItems';

import { 
  IconLink, 
  IconButton, 
  useSliceStore, 
  useSliceSelector,
  Spiner
} from 'utils/helper';

import { NAME_SPACE } from 'redux/reducers/purchase/voucher/formReducer';

const itemName = 'chứng từ mua hàng';

export default function VoucherForm({id, update, readOnly}){
  const baseUrl = '/purchase/voucher/api';
  const backUrl = (update || readOnly)? '../' : '../voucher';
  const editUrl = id? `../update/${id}` : null;
  
  const router = useRouter();
  const store = useSliceStore(NAME_SPACE);
  const [data] = useSliceSelector(NAME_SPACE, ['data']);
  
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
          
          <Tabs className="mt-3">
            <Tab eventKey="goodsItems" title="Hàng hoá/dịch vụ">
              <GoodItems readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="taxItems" title="Thuế">
              <TaxItems readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="foreignTaxItems" title="Phí hải quan">
              <div>Phí hải quan</div>
            </Tab>
            <Tab eventKey="expenseItems" title="Chi phí">
              <div>Chi phí</div>
            </Tab>
          </Tabs>

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