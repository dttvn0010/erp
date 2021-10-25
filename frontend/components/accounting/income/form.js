import Card from 'components/share/card';
import { 
  IconLink, 
  IconButton
} from 'utils/helper';

const itemName = 'tiền thu';

export default function IncomeForm({id, update, readOnly}){
  const title = (
    readOnly? `Xem ${itemName}` : (update? `Cập nhập ${itemName}` : `Tạo mới ${itemName}`)
  );
  const backUrl = (update || readOnly)? '../' : '../income';
  const editUrl = id? `../update/${id}` : null;

  const saveIncome = () => {};
  return (
    <Card
      title={title}
      body={
        <form id="fmt" onSubmit={saveIncome}>
          
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