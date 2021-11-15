import axios from 'axios';
import { useEffect } from 'react';
import { useRouter } from 'next/router';

import { Tab, Tabs } from 'react-bootstrap';
import Card from 'components/share/card';
import Input from "components/share/input";
import ErrorList from "components/share/errorlist";

import ReceiptNote from '../sections/note/receiptNote';
import DebtDeductNote from '../sections/note/debtDeductNote';
import OutStockNote from '../sections/note/outStockNote';

import GoodItems from '../sections/itemList/goodsItems';

import { 
  IconLink, 
  IconButton, 
  useSliceStore, 
  useSliceSelector,
  Spiner
} from 'utils/helper';

import { NAME_SPACE } from 'redux/reducers/purchase/return/formReducer';

const itemName = 'chứng từ trả lại hàng mua';

export default function ReturnForm({id, update, readOnly}){
  const baseUrl = '/purchase/return/api';
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

  const saveReturn = async (e) => {
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
        <form id="fmt" onSubmit={saveReturn}>
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
                        value={data.supplier}
                        onChange={(val) => updateData({supplier: val})}
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
              <div className="section-title">Thông tin chứng từ</div>
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
            <Tab eventKey="outStockNote" title="Phiếu xuất">
              <OutStockNote readOnly={readOnly}/>
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