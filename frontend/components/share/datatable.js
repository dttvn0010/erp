import axios from 'axios';
import React, { useEffect, useReducer, useState } from 'react';
import {Dropdown} from "react-bootstrap";
import Input from "components/share/input";
import {appendUrlParams} from "utils/helper";

function compareRowByCol(row1, row2, colName) {
  if(row1[colName] < row2[colName]){
    return -1;
  }
  if(row1[colName] > row2[colName]) {
    return 1;
  }
  return 0;
}

function orderRows(rows, colName, asc) {
  if(!colName) {
    return rows;
  }
  let sign = asc ? 1 : -1;
  return rows.sort((r1, r2) => sign * compareRowByCol(r1, r2, colName));
}

const FilterToggle = React.forwardRef(({ children, onClick }, ref) => (
  <span
    href=""
    ref={ref}
    onClick={(e) => {
      e.preventDefault();
      onClick(e);
    }}
  >
    {children}
  </span>
));

function FilterButton({col, table, dispatch}) {
  let colName = col.data;
  let searchActive = table.searchActive[colName];
  let [searchValue, setSearchValue] = useState('');
  let [fromDate, setFromDate] = useState('');
  let [toDate, setToDate] = useState('');
  let [selectedOptions, setSelectedOptions] = useState([]);

  let options = (col.displayList || []).map(item => (
    {
      name: item[1],
      value: item[0]
    }
  ));
  
  let getSelectedIds = () => {
    return selectedOptions.map(opt => opt.value).join(",");
  }

  return (
    <Dropdown className={`filter ${searchActive? 'active': ''}` }>
      <Dropdown.Toggle as={FilterToggle}>
        <i className="fas fa-filter" ></i>
      </Dropdown.Toggle>

      <Dropdown.Menu className="inline-editor p-1">
        {(col.dtype === 'text' || col.dtype === "number") &&
          <div className="full-width dropdown-keep-open">
            <label className="mb-1">Nhập giá trị để tìm:</label>
            <input 
              type={col.dtype}
              className="full-width text-filter" 
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
            />
            <button 
              className="mt-1 btn btn-sm btn-success btn-filter btn-filter-text"
              onClick={() => dispatch.filterTableBy(colName, searchValue)}
            >
              <i className="fas fa-check"></i>
            </button>
          </div>
        }

        {col.dtype === 'bool' &&
          <div className="full-width dropdown-keep-open p-2">
            <div className="radio-group">
              <div className="mb-2">
                <input 
                  type="radio"
                  checked={searchValue===""}
                  onClick={() => setSearchValue("")}
                  name={`input-filter-${colName}`}
                />
                <label>Tất cả</label>
              </div>
              <div className="mb-2">
                <input 
                  type="radio"
                  checked={searchValue===1}
                  onClick={() => setSearchValue(1)}
                  name={`input-filter-${colName}`}
                />
                <label>Có</label>
              </div>
              <div className="mb-2">
                <input 
                  type="radio"
                  checked={searchValue===0}
                  onClick={() => setSearchValue(0)}
                  name={`input-filter-${colName}`}
                />
                <label>Không</label>
              </div>
            </div>
            <button 
              className="mt-1 btn btn-sm btn-success btn-filter btn-filter-bool" 
              onClick={() => dispatch.filterTableBy(colName, searchValue)}
            >
              <i className="fas fa-check"></i>
            </button>
          </div>
        }

        {(col.dtype === 'date' || col.dtype === 'datetime') &&
          <div className="full-width dropdown-keep-open">
            <div className="d-flex">
              <div className="half-width px-1">
                <label className="mb-1">Từ ngày:</label>
                <Input
                  type="date"
                  value={fromDate}
                  onChange={val => setFromDate(val)}
                />
              </div>

              <div className="half-width px-1">
                <label className="mb-1">Đến ngày:</label>
                <Input
                  type="date"
                  value={toDate}
                  onChange={val => setToDate(val)}
                />
              </div>
            </div>
            <button 
              className="mt-1 btn btn-sm btn-success btn-filter btn-filter-date"
              onClick={() => dispatch.filterTableBy(colName, `${fromDate}--${toDate}`)}
            >
              <i className="fas fa-check"></i>
            </button>
          </div>
        }

        {(col.dtype === 'category' || col.dtype === 'multiCategory') &&
          <div className="full-width dropdown-keep-open">
            <label className="mb-1">Chọn giá trị để tìm:</label>
            
            {!col.asyncSearch &&
              <Input type="select"
                isMulti={true}
                value={selectedOptions}
                onChange={val => setSelectedOptions(val)}
                options={options}
              />
            }
            {col.asyncSearch &&
              <Input
                type="async-select"
                isMulti={true}
                value={selectedOptions}
                onChange={val => setSelectedOptions(val)}
                optionsUrl={appendUrlParams(table.apiUrl, {search_col: colName})}
              /> 
            }
            
            <button 
              className="mt-1 btn btn-sm btn-success btn-filter btn-filter-text"
              onClick={() => dispatch.filterTableBy(colName, getSelectedIds())}
            >
              <i className="fas fa-check"></i>
            </button>
          </div>
        }

      </Dropdown.Menu>
    </Dropdown>
  )
}

function OrderButton({colName, table, dispatch}) {
  let orderDir = table.orderDir??'asc';
  let active = colName === table.orderBy;
  let arrowDown = orderDir === 'desc' && colName === table.orderBy;
  
  return (
    <span className={`btn-sort sort-${orderDir} ${active?'active':''}`} 
      onClick={() => dispatch.sortTableBy(colName)}
    >
      {arrowDown && <span>&#x2193;</span>}
      {!arrowDown && <span>&#x2191;</span>}
    </span>
  )
}

function TableHead({table, dispatch}) {
  return (
    <thead>
      <tr>
        {table.columnsDef.map((col, i) => 
          <th key={i} style={{width: col.width}} className={col.cssClass}>
            {!col.isNarrow &&
              <div className="d-flex flex-row">
                <div style={{flex:1}}>{col.title}</div>
                <div>
                  {col.search &&
                    <FilterButton 
                      col={col} 
                      table={table} 
                      dispatch={dispatch}
                    />
                  }
                  {col.orderable &&(
                    <OrderButton 
                      colName={col.data} 
                      table={table} 
                      dispatch={dispatch}
                    />
                  )}
                </div>
              </div>
            }
            {col.isNarrow&&
              <div>
                <div>{col.title}</div>
                <div>
                  {col.search &&
                    <FilterButton 
                      col={col} 
                      table={table} 
                      dispatch={dispatch}
                    />
                  }
                  {col.orderable &&(
                    <OrderButton 
                      colName={col.data} 
                      table={table} 
                      dispatch={dispatch}
                    />
                  )}
                </div>
              </div>
            }
          </th>
        )}
      </tr>
    </thead>
  )
}

function TableRow({rowIndex, table, renders, dispatch}) {
  let {columnsDef, rows} = table;
  let row = rows[rowIndex];
  
  return (
    <tr key={rowIndex}>
      {columnsDef.map((col, j) =>
        <td key={j} className={col.cssClass}>
          {renders[`col${j}`] && renders[`col${j}`](row[col.data], row, dispatch)}
          {!renders[`col${j}`] && col.dtype !== 'bool' && <span>{row[col.data]}</span>}
          {!renders[`col${j}`] && col.dtype === 'bool' && 
            <input type="checkbox" checked={row[col.data]}/>
          }
        </td>
      )}
    </tr>
  )
}

function TableBody({table, renders, dispatch}) {
  let {rows, columnsDef} = table;

  return (
    <tbody>
      {rows.map((_, i) =>
        <TableRow 
          key={i} 
          rowIndex={i} 
          table={table}
          renders={renders}
          dispatch={dispatch}
        />
      )}

      {rows.length === 0 &&
        <tr>
          <td colSpan={columnsDef.length}>
            <label>Không có kết quả nào</label>
          </td>
        </tr>
      }
    </tbody>
  )
}

async function getColumnsDef(apiUrl) {
  apiUrl = appendUrlParams(apiUrl, {__meta__: 'true'});
  let result = await axios.get(apiUrl);
  return result.data || [];
} 

async function getDataSource({apiUrl, searchParams, orderBy, orderDir, page, pageSize}) {
  page = page || 1;
  searchParams = searchParams || {};
  let params = {};

  for (let [colName, searchValue] of Object.entries(searchParams)) {
    params[`columns[${colName}][search]`] = searchValue;
  }
  params.start = (page - 1) * pageSize;
  params.length = pageSize;
  
  if(orderBy){
    params.order_by = orderBy;
  }

  if(orderDir) {
    params.order_dir=orderDir;
  }

  apiUrl = appendUrlParams(apiUrl, params);

  console.log('apiUrl=', apiUrl);
  let result = await axios.get(apiUrl);
  return result.data || [];
}

function Pagination({page, total, pageSize, dispatch}) {
  let start = (page - 1) * pageSize;
  let end = Math.min(start + pageSize, total);
  start = Math.min(1+start, total);
  let numPages = Math.ceil(total / pageSize);

  return(
    <div>
      <span>Hiển thị {start}-{end} trên tổng số {total} kết quả</span>
      <div className="float-end d-flex">
        <div className="pe-4">
          <span>Kích thước trang: </span>
          <select 
            className="page-size-select" 
            value={pageSize}
            onChange={e => dispatch.setPageSize(e.target.value)}
          >
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
        </div>
        <ul className="pagination">
          <li className={"page-item " + ((page === 1)? "disabled": "")} 
            onClick={() => {if(page > 1) dispatch.setPage(1)}}
          >
            <a className="page-link" href="#/">
              &laquo;
            </a>
          </li>
          
          {(page == numPages && page >= 5) &&
            <li className="page-item" onClick={() => dispatch.setPage(page-4)}>
              <a className="page-link" href="#/">
                {page - 4}
              </a>
            </li>
          }

          {(page + 1 >= numPages && page >= 4) &&
            <li className="page-item" onClick={() => dispatch.setPage(page-3)}>
              <a className="page-link" href="#/">
                {page - 3}
              </a>
            </li>
          }

          {page >= 3 &&
            <li className="page-item" onClick={() => dispatch.setPage(page-2)}>
              <a className="page-link" href="#/">
                {page - 2}
              </a>
            </li>
          }

          {page >= 2 &&
            <li className="page-item" onClick={() => dispatch.setPage(page-1)}>
              <a className="page-link" href="#/">
                {page - 1}
              </a>
            </li>
          }

          <li className="page-item active">
            <a className="page-link">{page}</a>
          </li>
          
          {page < numPages &&
            <li className="page-item" onClick={() => dispatch.setPage(page+1)}>
              <a className="page-link" href="#/">
                {page + 1}
              </a>
            </li>
          }

          {page + 2 <= numPages &&
            <li className="page-item" onClick={() => dispatch.setPage(page+2)}>
              <a className="page-link" href="#/">
                {page + 2}
              </a>
            </li>
          }

          {(page <= 2 && page + 3 <= numPages)  &&
            <li className="page-item" onClick={() => dispatch.setPage(page+3)}>
              <a className="page-link" href="#/">
                {page + 3}
              </a>
            </li>
          }

          {(page <= 1 && page + 4 <= numPages) &&
            <li className="page-item" onClick={() => dispatch.setPage(page+4)}>
              <a className="page-link" href="#/">
                {page + 4}
              </a>
            </li>
          }

          <li className={"page-item " + ((page === numPages)? "disabled": "")} 
            onClick={() => {if(page < numPages) dispatch.setPage(numPages)}}
          >
            <a className="page-link" href="#/">
              &raquo;
            </a>
          </li>        
        </ul>
      </div>
    </div>
  )
}

export default function DataTable({apiUrl, renders}) {
  renders = renders || {};

  let [table, updateTable] = useReducer(
    (state, newState) => ({...state, ...newState}),
    {
      apiUrl: apiUrl,
      loading: true,
      columnsDef: [],
      rows: [],
      searchParams: {},
      searchActive: {},
      orderDir: 'asc',
      orderBy: '',
      page: 1,
      pageSize: 10,
      total: 0
    }
  );

  useEffect(async () => {
    let columnsDef = await getColumnsDef(apiUrl);
    updateTable({columnsDef: columnsDef})

    let {data, total} = await getDataSource({
      apiUrl,
      page: 1,
      pageSize: 10
    });

    updateTable({rows: data, total, loading: false});
  }, [])
  
  const dispatch = {
    async fetchData({searchParams, orderBy, orderDir, page, pageSize}) {
      if(searchParams !== null) {
        searchParams = {...table.searchParams, ...searchParams};  
      }
      
      orderBy = orderBy || table.orderBy;
      orderDir = orderDir || table.orderDir;
      page = page || table.page;
      pageSize = pageSize || table.pageSize;

      updateTable({loading: true});

      let {data, total} = await getDataSource({
        apiUrl,
        page,
        pageSize: pageSize,
        searchParams: searchParams,
        orderBy: orderBy,
        orderDir: orderDir
      });

      updateTable({
        rows: data, 
        total, 
        loading: false, 
        page,
        pageSize,
        searchParams,
        orderBy,
        orderDir
      });

    },

    async reload() {
      updateTable({searchActive: {}});

      this.fetchData({
        page: 1,
        pageSize: 10,
        orderBy: '',
        orderDir: '',
        searchParams: null
      });
    },

    async refresh() {
      this.fetchData({searchParams: {}});
    },

    async setPage(page) {
      this.fetchData({page});
    },

    async setPageSize(pageSize) {
      this.fetchData({
        page: 1,
        pageSize
      })
    },

    async filterTableBy(colName, searchValue){
      let searchActive = table.searchActive;
      searchActive[colName] = searchValue !== '';
      
      updateTable({searchActive});

      this.fetchData({
        page: 1, 
        searchParams: {[colName]: searchValue}
      })
    },
    
    sortTableBy(colName) {
      let asc = true;
    
      if(colName === table.orderBy) {
        asc = !(table.orderDir === 'asc')
      }

      this.fetchData({
        page: 1, 
        orderBy: colName, 
        orderDir: asc? 'asc': 'desc'
      });
    },
  };

  if(!table.columnsDef || table.columnsDef.length === 0) {
    //return <></>;
  }

  return (
    <div className="table-responsive">
      <button 
        className="btn btn-sm float-end btn-reload"
        onClick={() => dispatch.reload()}
      >
        <i className="fas fa-sync" ></i>
      </button>
      
      <table className="mt-2 table table-bordered data-table">
        <TableHead 
          table={table} 
          dispatch={dispatch}
        />

        {table.loading &&
          <tbody>
            <tr>
              <td colSpan={table.columnsDef.length} className="text-center">
                <div className="spinner-border" role="status">
                  <span className="sr-only"></span>
                </div>
              </td>
            </tr>
          </tbody> 
        }

        {!table.loading &&
          <TableBody 
            table={table} 
            renders={renders}
            dispatch={dispatch}
          />
        }
      </table>

      <Pagination 
        page={table.page} 
        pageSize={table.pageSize} 
        total={table.total}
        dispatch={dispatch}
      />
    </div>
  );
}