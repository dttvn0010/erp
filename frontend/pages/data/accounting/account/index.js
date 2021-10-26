import axios from 'axios';
import { Modal, Button } from 'react-bootstrap';
import { EllipsisDropDown } from 'components/share/ellipsisDropdown';
import Card from 'components/share/card';
import DataTable from 'components/share/datatable';
import { useSliceSelector, useSliceStore } from 'utils/helper';
import { NAME_SPACE } from 'redux/reducers/data/accounting/account/indexReducer';

import { 
  getDefaultLayOut,
} from 'utils/helper';
import Input from 'components/share/input';

function BalanceModal() {
  const [accountNumber,   balance,   showBalanceModal] = useSliceSelector(NAME_SPACE, 
        ['accountNumber', 'balance', 'showBalanceModal']);
  
  const store = useSliceStore(NAME_SPACE);
  const handleClose = () => store.setState({showBalanceModal: false});
  
  const handleSave = () => {
    const {accountId, balance, dispatch} = store.getState();
    
    axios.patch(`/accounting/account/update-balance/${accountId}`, {balance}).then(_ => {
      store.setState({showBalanceModal: false});
      if(dispatch) dispatch.refresh();

    }).catch(_ => {
      alert('Lỗi xảy ra khi cập nhật số dư');
    })
  }
  
  return (
    <Modal show={showBalanceModal} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Số dư tài khoản {accountNumber}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <form id="fmt">
          <Input 
            type="number"
            value={balance}
            onChange={val => store.setState({balance:val})}
          />
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Đóng lại
        </Button>
        <Button variant="primary" onClick={handleSave}>
          Lưu lại
        </Button>
      </Modal.Footer>
    </Modal>
  )
}

export default function Index() {
  
  const itemName = 'tài khoản kế toán';
  const baseUrl = '/accounting/account';
  
  const store = useSliceStore(NAME_SPACE);

  let renders = {
    col4: (_, row, dispatch) => {
      let items = [
        {
          title: 'Nhập số dư',
          onClick: () => {
            store.setState({
              dispatch: dispatch,
              accountId: row.id,
              accountNumber: row.code,
              showBalanceModal: true,
              balance: row.balance
            })
          }
        },
      ];

      return (
        <EllipsisDropDown 
          items={items}
        />
      )
    }
  }

  return (
    <>
      <Card
      title={`Danh sách ${itemName}`}
        body={
          <>
            <DataTable 
              renders={renders}
              apiUrl={`${baseUrl}/search`}
            />
          </>
        }
      />
      <BalanceModal/>
    </>
  )
}

Index.getLayout = getDefaultLayOut;