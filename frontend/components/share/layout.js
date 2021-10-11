import React, {useState} from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import {Dropdown} from 'react-bootstrap'
import { useSliceSelector, useSliceStore } from 'utils/helper'

const pages = [
  {path: '/', title: 'Trang chủ'},
  /*
  {
    path: '/employee', title: 'Quản lý nhân viên', 
    children: [
      {path: '/user', title: 'Tài khoản người dùng'},
      {path: '/role', title: 'Vai trò'},
      {path: '/department', title: 'Phòng ban'},
      {path: '/team', title: 'Nhóm làm việc'},
    ]
  },*/
  {
    path: '/purchase', title: 'Mua hàng',
    children: [
      {path: '/order', title: 'Phiếu mua hàng'}
    ] 
  },
  {
    path: '/sales', title: 'Bán hàng',
    children: [
      {path: '/order', title: 'Phiếu bán hàng'}
    ] 
  },
  {
    path: '/stock', title: 'Kho',
  },
  {
    path: '/data', title: 'Danh mục',
    children: [
      {path: '/category', title: 'Nhóm hàng hoá/dịch vụ'},
      {path: '/product', title: 'Hàng hoá/dịch vụ'},
      {path: '/partner', title: 'Khác hàng/nhà cung cấp'},
      {path: '/location', title: 'Địa điểm kho'},
    ]
  }
]

function usePathActive(path) {
  const router = useRouter();

  if(!path.endsWith('/')) {
    path += '/';
  }
  
  let active = (router.pathname + '/').startsWith(path);
  
  if(path == '/') {
    active = router.pathname === '/'
  }

  return active;
}

function useNavLinkClass(path){
  if(usePathActive(path)) {
    return "nav-link active";
  }else{
    return "nav-link";
  }
}

const MenuToggle = React.forwardRef(({ children, onClick }, ref) => (
  <a
    className="nav-link dropdown-toggle"
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

function MenuDropDown({page}) {
  const store = useSliceStore('app');
  const [selectedPage] = useSliceSelector('app', ['selectedPage']);

  const [expanded, setExpanded] = useState(usePathActive(page.path));
  const children = page.children;

  const toggleCollapse = () => {

    if(selectedPage !== page.path || !expanded) {
      setExpanded(true);
      store.setState({selectedPage: page.path});
    }else{
      setExpanded(false);
      store.setState({selectedPage: null});
    }
  }

  const show = (selectedPage === page.path);

  return (
    <>
      <a className={useNavLinkClass(page.path) + (show? "": " collapsed")} href="#" aria-expanded="false"
        onClick={toggleCollapse}
      >
        {page.title}
        <div className="sb-sidenav-collapse-arrow"><i className="fas fa-angle-down"></i></div>
      </a>
      <div className={"collapse " + (show? "show": "")}>
        <nav className="sb-sidenav-menu-nested nav">
          {children.map((child_page, index) => 
            <Link href={page.path + child_page.path} key={index}>
              <a className={useNavLinkClass(page.path + child_page.path)}>
                {child_page.title}
              </a>
            </Link>
          )}
        </nav>
      </div>
    </>
  )
}

export default function Layout({ children }) {
  const [toggled, setToggled] = useState(false);
  const store = useSliceStore('app');
  
  return (
    <body 
      className={"sb-nav-fixed " + (toggled?"sb-sidenav-toggled" : "")}
    > 
      <nav className="sb-topnav navbar navbar-expand navbar-dark bg-dark">
        <a className="navbar-brand ps-3" href="index.html">ERP</a>
        <button 
          id="sidebarToggle"
          className="btn btn-link btn-sm order-1 order-lg-0 me-4 me-lg-0"
          onClick={() => setToggled(!toggled)}
        >
          <i className="fas fa-bars"></i>
        </button>
        
        <form className="d-md-inline-block form-inline ms-auto me-0 me-md-3 my-2 my-md-0">
          <div className="input-group">
            <input className="form-control" type="text" placeholder="Tìm kiếm..." aria-describedby="btnNavbarSearch" />
            <button className="btn btn-primary" id="btnNavbarSearch" type="button"><i className="fas fa-search"></i></button>
          </div>
        </form>
        
        <ul className="navbar-nav ms-auto ms-md-0 me-3 me-lg-4">
          <Dropdown>
            <Dropdown.Toggle as={MenuToggle}>
              <i className="fas fa-user fa-fw"></i>
            </Dropdown.Toggle>

            <Dropdown.Menu>
              <Dropdown.Item href="#/">Logout</Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </ul>
      </nav>

      <div id="layoutSidenav">
        <div id="layoutSidenav_nav">
          <nav className="sb-sidenav accordion sb-sidenav-dark" id="sidenavAccordion">
            <div className="sb-sidenav-menu">
              <div className="nav">
                {pages.map((page, index) => 
                  <>
                    {page.children && <MenuDropDown page={page}/>}
                    {!page.children &&
                      <Link 
                        href={page.path} 
                        key={index}
                      >
                        <a  
                          className={useNavLinkClass(page.path)}
                          onClick={() => store.setState({selectedPage: page.path})}
                        >
                          {page.title}
                        </a>
                      </Link>
                    }
                  </>
                )}
              </div>
            </div>
          </nav>
        </div>
        <div id="layoutSidenav_content">
          <main>{children}</main>
          <footer className="py-4 bg-light mt-auto">
            <div className="container-fluid px-4">
              <div className="d-flex align-items-center justify-content-between small">
                <div className="text-muted">Bản quyền @ thuộc về ...</div>
                <div>
                  <a href="#">Chính sách riêng tư</a>
                  &middot;
                  <a href="#">Điều khoản sử dụng</a>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </div>
    </body>
  )
}