import axios from 'axios';
import { useEffect } from 'react';
import { useRouter } from 'next/router';

import { Tab, Tabs } from 'react-bootstrap';
import Card from 'components/share/card';
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

import { NAME_SPACE } from 'redux/reducers/purchase/discount/formReducer';

const itemName = 'chứng từ giảm giá hàng mua';

export default function DiscountForm({id, update, readOnly}){
  const baseUrl = '/purchase/discount/api';
  const backUrl = (update || readOnly)? '../' : '../discount';
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

  const saveDiscount = async (e) => {
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
        <form id="fmt" onSubmit={saveDiscount}>
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
          
          <Tabs className="mt-3">
            <Tab eventKey="goodsItems" title="Hàng hoá/dịch vụ">
              <GoodItems readOnly={readOnly}/>
            </Tab>
            <Tab eventKey="misc" title="Khác">
              <div>Khác</div>
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