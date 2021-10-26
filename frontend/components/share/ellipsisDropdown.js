import MenuToggle from './toggle'
import { Dropdown } from 'react-bootstrap'

export function EllipsisDropDown({items}) {
  return(
    <Dropdown>
      <Dropdown.Toggle as={MenuToggle}>
        <i className="fas fa-ellipsis-v"></i>
      </Dropdown.Toggle>

      <Dropdown.Menu>
        {items.map((item, index) =>
          <Dropdown.Item key={index} href="#/" onClick={item.onClick}>
            {item.title}
          </Dropdown.Item>
        )}
      </Dropdown.Menu>
    </Dropdown>
  )
}