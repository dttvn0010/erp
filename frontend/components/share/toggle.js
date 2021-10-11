import React from 'react'

const MenuToggle = React.forwardRef(({ children, onClick }, ref) => (
  <a
    href="#/"
    ref={ref}
    onClick={(e) => {
      e.preventDefault();
      onClick(e);
    }}
  >
    {children}
  </a>
));
  
export default MenuToggle;