import Card from 'components/share/card';
import { 
  IconLink, 
  IconButton
} from 'utils/helper';

const itemName = 'chi phí';

export default function ExpenseForm({id, update, readOnly}){
  const title = (
    readOnly? `Xem ${itemName}` : (update? `Cập nhập ${itemName}` : `Tạo mới ${itemName}`)
  );
  const backUrl = (update || readOnly)? '../' : '../expense';
  const editUrl = id? `../update/${id}` : null;

  const saveExpense = () => {};
  return (
    <Card
      title={title}
      body={
        <form id="fmt" onSubmit={saveExpense}>
          
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