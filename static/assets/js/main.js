function updateDatePicker() {
  setTimeout(() => {
    $('.date-picker').each(function () {
      let format = $(this).attr('data-format') || 'dd/mm/yyyy';
      $(this).datepicker({ format, language: 'vi' });
    });
  }, 200);
};

function $_get(url) {
  return fetch(url);
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function $_post(url, params) {
  var headers = {'X-CSRFToken': getCookie('csrftoken')};

  var data;

  if (params instanceof FormData) {
    data = params;
  } else {
    data = new FormData();

    if (params) {
      Object.keys(params).forEach(function (key) {
        data.append(key, params[key]);
      });
    }
  }

  return fetch(url, { method: "POST", body: data, headers });
}

function formatThousand(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

const PAGE_SIZE = 5;

function renderTableHead(table) { //columnsDef, params, orderBy, orderDir
  return (
    `<thead>
        <tr>` + table.columnsDef.map(col => `
          <th ${col.width ? `style="width:${col.width}"` : ''} 
            class='${col.cssClass ?? ""}'
          >
            ${col.title}

            <div class="float-end">
              ${col.search ?
                `<span class="filter ${table.params[`columns[${col.data}][search]`]?'active':''}">
                  <span data-bs-toggle="dropdown"><i class="fas fa-filter" ></i></span> 
                  <div class="dropdown-menu inline-editor p-1">
                    
                    ${col.dtype == 'text'?
                      `<div class="full-width dropdown-keep-open">
                        <label class="mb-1">Nhập giá trị để tìm:</label>
                        <input type="text" class="full-width" value="${table.params[`columns[${col.data}][search]`]??''}"/>
                        <button class="mt-1 btn btn-sm btn-success btn-filter btn-filter-text" data-col='${col.data}'>
                          <i class="fas fa-check"></i>
                        </button>
                      </div>`: ''
                    }

                    ${col.dtype == 'bool'?
                      `<div class="full-width dropdown-keep-open p-2">
                        <div class="radio-group">
                          <div class="mb-2">
                            <input type="radio" value="" ${(table.params[`columns[${col.data}][search]`]??'')==''? 'checked':''} 
                              name="input-filter-${col.data}">

                            <label>Tất cả</label>
                          </div>
                          <div class="mb-2">
                            <input type="radio" value="1" ${(table.params[`columns[${col.data}][search]`]??'')=='1'? 'checked':''} 
                              name="input-filter-${col.data}">

                            <label>Có</label>
                          </div>
                          <div class="mb-2">
                            <input type="radio" value="0" ${(table.params[`columns[${col.data}][search]`]??'')=='0'? 'checked':''}
                              name="input-filter-${col.data}">
                            <label>Không</label>
                          </div>
                        </div>
                        <button class="mt-1 btn btn-sm btn-success btn-filter btn-filter-bool" data-col='${col.data}'>
                          <i class="fas fa-check"></i>
                        </button>
                      </div>`:``
                    }

                    ${col.dtype == 'date' || col.dtype == 'datetime'?
                      `<div class="full-width dropdown-keep-open">
                        <div class="row">
                          <div class="col-6 pe-1">
                            <label class="mb-1">Từ ngày:</label><br>
                            <input type="text" value="${(table.params[`columns[${col.data}][search]`]??'--').split('--')[0]}" />
                          </div>

                          <div class="col-6 ps-1">
                            <label class="mb-1">Đến ngày:</label><br>
                            <input type="text" value="${(table.params[`columns[${col.data}][search]`]??'--').split('--')[1]}" />
                          </div>
                        </div>
                        <button class="mt-1 btn btn-sm btn-success btn-filter btn-filter-date" data-col='${col.data}'>
                          <i class="fas fa-check"></i>
                        </button>
                      </div>`: ''
                    }

                    ${col.dtype == 'category' || col.dtype == 'multiCategory'?
                      `<div class="full-width">
                        <label class="mb-1">Nhập giá trị để tìm:</label>
                        <select ${col.asyncSearch? `async data-col=${col.data}`:''} multiple class="full-width dropdown-keep-open">
                          ${col.display_list.map(item =>( 
                            `<option value="${item[0]}"
                              ${(table.params[`columns[${col.data}][search]`]??[]).includes((item[0]??'').toString())?'selected':''}
                            >
                              ${item[1]}
                            </option>`)
                          ).join('')}
                        </select>
                        
                        <button class="mt-1 btn btn-sm btn-success btn-filter btn-filter-list" data-col='${col.data}'>
                          <i class="fas fa-check"></i>
                        </button>
                      </div>`: ''
                    }
                  </div>
                </span>` : ''
              }
              
              ${col.orderable ?
                `<span class="btn-sort sort-${table.orderDir??'asc'} ${col.data==table.orderBy?'active':''}" 
                  data-col='${col.data}'
                >
                  <i class="fas fa-arrow-${table.orderDir=='desc' && col.data==table.orderBy?'down':'up'}"></i>
                </span>`: ''
              }
            </div>
          </th>
        `).join('') +
    `</tr>
      </thead>`
  )
}

function renderTableBody(columnsDef, rows) {
  if (rows.length == 0) {
    return (
      `<tbody>
          <tr>
            <td colspan="${columnsDef.length}">Không có kết quả nào</td>
          </tr>
        </tbody>`
    )
  }
  return (
    `<tbody>` + rows.map((row,i) => `
        <tr>
          ${columnsDef.map(col => `
            <td class='${col.cssClass ?? ""}'>
              ${col.render ? col.render(row[col.data], row) :
                (col.editable? 
                  (col.dtype != 'bool'?
                    `<a href='javascript:void(0)' data-bs-toggle="dropdown">
                      ${(Array.isArray(row[col.data])? row[col.data].join(', '): row[col.data] ?? '') || '<i class="fas fa-edit"></i>'}
                    </a>
                    <div class="dropdown-menu inline-editor p-1">
                      <div class="full-width">
                        <label class="mb-1">Nhập giá trị mới:</label>
                        ${col.dtype == 'text' && col.editWidget == 'input'?
                          `<input type="text" class="full-width inline-editor-value" value="${row[col.data]??''}"/>`: ''
                        }

                        ${col.dtype == 'text' && col.editWidget == 'textarea'?
                          `<textarea rows="5" class="full-width inline-editor-value">${row[col.data]??''}</textarea>`: ''
                        }

                        ${col.dtype == 'date' ?
                          `<input type="text" class="date-picker full-width inline-editor-value" value="${row[col.data]??''}"/>`: ''
                        }

                        ${col.dtype == 'datetime'?
                          `<input type="text" class="date-time-picker full-width inline-editor-value" value="${row[col.data]??''}"/>`: ''
                        }

                        ${col.dtype == 'category' ?
                          `<select ${col.asyncSearch? `async data-col=${col.data}`:''} class="full-width inline-editor-value">
                            ${col.blank?
                              `<option value>---------</option>`:''
                            }
                            ${col.display_list.map(item => 
                              `<option value="${item[0]}" ${item[0]==row[col.data + '_id']?'selected':''}>
                                ${item[1]}
                              </option>`
                            )}
                          </select>`: ''
                        }

                        ${col.dtype == 'multiCategory' ?
                          `<select ${col.asyncSearch? `async data-col=${col.data}`:''} class="full-width inline-editor-value" multiple>
                            ${col.display_list.map(item => 
                              `<option value="${item[0]}" ${(row[col.data + '_id']??[]).includes(item[0].toString())?'selected':''}>
                                ${item[1]}
                              </option>`
                            )}
                          </select>`: ''
                        }
                      </div>
                      <button class="mt-1 btn btn-sm btn-success btn-update" data-col="${col.data}" data-row="${i}">
                        <i class="fas fa-check"></i>
                      </button>
                    </div>`
                    :`
                    <input type="checkbox" ${row[col.data]?'checked':''} class="inline-editor-checkbox"
                      data-col="${col.data}" data-row="${i}">
                    `
                  ) 
                  :
                  (col.dtype == 'bool'?
                    `<input type="checkbox" ${row[col.data]?'checked':''} onclick="return false">`:
                    (Array.isArray(row[col.data])? row[col.data].join('-'): row[col.data] ?? '')
                  )
                )
              } 
            </td>
          `).join('')}
        </tr>`).join('') +
    `</tbody>`
  );
}

function renderPagination(page, total, pageSize) {
  const start = (page - 1) * pageSize;
  const end = Math.min(start + pageSize, total);
  let numPages = Math.ceil(total / pageSize);

  
  return (
    `<div>
        <span>Hiển thị ${start + 1}-${end} trên tổng số ${total} kết quả</span>
        <div class="float-end d-flex">
          <div class="pe-4">
            <span>Kích thước trang:</span>
            <select class="page-size-select">
              <option ${pageSize==10?'selected':''}>10</option>
              <option ${pageSize==2?'selected':''}>2</option>
              <option ${pageSize==5?'selected':''}>5</option>
              <option ${pageSize==20?'selected':''}>20</option>
            </select>
          </div>
          <ul class="pagination">
            <li class="page-item ${page == 1 ? 'disabled' : ''}">
              <a class="page-link" ${page>1?`data-page="1" href="javascript:void(0)"`:''}>
                &laquo;
              </a>
            </li>
            
            ${(page == numPages && page >= 5) ? `
              <li class="page-item">
                <a class="page-link" data-page="${page-4}" href="javascript:void(0)">
                  ${page - 4}
                </a>
              </li>`: ''
            }

            ${(page + 1 >= numPages && page >= 4) ? `
              <li class="page-item">
                <a class="page-link" data-page="${page-3}" href="javascript:void(0)">
                  ${page - 3}
                </a>
              </li>`: ''
            }

            ${page >= 3 ? `
              <li class="page-item">
                <a class="page-link" data-page="${page-2}" href="javascript:void(0)">
                  ${page - 2}
                </a>
              </li>`: ''
            }

            ${page >= 2 ? `
              <li class="page-item">
                <a class="page-link" data-page="${page-1}" href="javascript:void(0)">
                  ${page - 1}
                </a>
              </li>`: ''
            }

            <li class="page-item active">
              <a class="page-link">${page}</a>
            </li>
            
            ${page < numPages ? `
              <li class="page-item">
                <a class="page-link" data-page="${page+1}" href="javascript:void(0)">
                  ${page + 1}
                </a>
              </li>`: ''
            }

            ${page + 2 <= numPages ? `
              <li class="page-item">
                <a class="page-link" data-page="${page+2}" href="javascript:void(0)">
                  ${page + 2}
                </a>
              </li>`: ''
            }

            ${(page <= 2 && page + 3 <= numPages) ? `
              <li class="page-item">
                <a class="page-link" data-page="${page+3}" href="javascript:void(0)">
                  ${page + 3}
                </a>
              </li>` : ''
            }

            ${(page <= 1 && page + 4 <= numPages) ? `
              <li class="page-item">
                <a class="page-link" data-page="${page+4}" href="javascript:void(0)">
                  ${page + 4}
                </a>
              </li>` : ''
            }

            <li class="page-item ${page == numPages ? 'disabled' : ''}">
              <a class="page-link" ${page < numPages ? `data-page="${numPages}" href="javascript:void(0)"` : ''}>
                &raquo;
              </a>
            </li>        
          </ul>
        </div>
      </div>`
  )
}

async function builTableHtml(table) {
  let apiUrl = table.apiUrl;

  if (!apiUrl.includes('?')) {
    apiUrl += '?'
  }

  for (let key in table.params) {
    apiUrl += `&${key}=${encodeURIComponent(table.params[key])}`;
  }

  let start = (table.page - 1) * table.pageSize;
  apiUrl += `&start=${start}&length=${table.pageSize}`;
  
  if(table.orderBy){
    apiUrl += `&order_by=${table.orderBy}`;
  }

  if(table.orderDir) {
    apiUrl += `&order_dir=${table.orderDir}`;
  }

  console.log('apiUrl=', apiUrl);

  let thead = renderTableHead(table);
  let resp = await $_get(apiUrl);
  let data = await resp.json();
  let rows = data.data || [];
  let tbody = renderTableBody(table.columnsDef, rows);
  let pagination = renderPagination(table.page, data.total, table.pageSize);

  let html = (
    `<table class="table table-bordered data-table">
        ${thead}
        ${tbody}
      </table>
      ${pagination}`
  );

  table.$el.html(html);
  table.rows = rows;
  
  table.$el.find('.btn-filter').each(function(){
    if($(this).hasClass('btn-filter-text')) {
      let colName = $(this).attr('data-col');
      
      if(colName) {
        let input = $(this).parent().children('input').first();

        let onClick = () => {
          let text = input.val().trim();
    
          if(text != '') {
            $(this).parents('.filter').first().addClass('active');
          }else {
            $(this).parents('.filter').first().removeClass('active');
          }
    
          table.searchBy(colName, text);
        };

        $(this).click(onClick);

        $(input).on("keydown", function(event) {
          if(event.which == 13){
            onClick();
          }
        });
      }

    }else if($(this).hasClass('btn-filter-bool')) {
      $(this).click(function() {
        let colName = $(this).attr('data-col');
        let value = $(`input[name=input-filter-${colName}]:checked`).val();
        table.searchBy(colName, value);
      });

    }else if($(this).hasClass('btn-filter-date')) {
      $(this).click(function() {
        let colName = $(this).attr('data-col');
        let inputs = $(this).parent().find('input');
        let values = [];

        inputs.each(function(){
          values.push($(this).val());
        });
        let value = values.join('--');
        table.searchBy(colName, value != '--'? value : '');
      });

    }else if($(this).hasClass('btn-filter-list')) {
      $(this).click(function() {
        let colName = $(this).attr('data-col');
        let select = $(this).parent().children('select').first();
        console.log(colName, select.val());
        table.searchBy(colName, select.val().join(','));
      });
    }
  });

  table.$el.find('.btn-sort').click(function(){
    let asc = true;
    let colName = $(this).attr('data-col');
    
    if(colName == table.orderBy) {
      asc = !$(this).hasClass('sort-asc');
    }
    
    table.sortBy(colName, asc ? 'asc' : 'desc');
  });

  table.$el.find('.btn-update').click(function(){
    let rowIndex = $(this).attr('data-row');
    let colName = $(this).attr('data-col');
    
    if(rowIndex && colName) {
      let input = $(this).parent().find('.inline-editor-value').first();
      table.updateField(rowIndex, colName, input.val()??'');
    }
  });

  table.$el.find('.inline-editor-checkbox').click(function(){
    if(!confirm('Bạn có muốn đổi trạng thái')){
      return false;
    }
    let checked = $(this).prop('checked');
    let colName = $(this).attr('data-col');
    let value = checked? 1 : 0;
    let rowIndex = $(this).attr('data-row');
    table.updateField(rowIndex, colName, value);
    return false;
  });

  table.$el.find('.page-link').click(function(){
    let page = $(this).attr('data-page');
    if(page){
      table.setPage(page);
    }
  });

  table.$el.find('.page-size-select').change(function(){
    let pageSize = $(this).val();
    table.setPageSize(pageSize);
  });

  table.$el.find('.date-picker').datepicker({language: 'vi', format: 'dd/mm/yyyy'});
  table.$el.find('.date-time-picker').datepicker({language: 'vi', format: 'dd/mm/yyyy'});
  table.$el.find('.data-table select').each(function(){
    if($(this).attr('async')) {
      let colName = $(this).attr('data-col');
      $(this).select2({
        allowClear: true,
        ajax: {
          url: table.apiUrl+ `?search_col=${colName}`,
          dataType: 'json',
          delay: 250,
        },
        placeholder: '',
        minimumInputLength: 1,
        templateResult: (item) => {
          if (item.loading) {
            return item.text;
          }
          return item.display;
        },
        templateSelection: (item) => item.display || item.text,
      })
    }else{
      $(this).select2();
    }
  });
  
  table.$el.find('.dropdown-keep-open, .select2-selection').click(function(e) {
    e.stopPropagation();
  });
}

async function getTableDef(el, apiUrl, renders, pageSize) {
  renders = renders || {};

  let resp = await $_get(apiUrl + '?__meta__=true');
  let data = await resp.json();
  let columnsDef = data || [];
  columnsDef.forEach((col, i) => {
    col.render = renders[`col${i}`];
  });

  return {
    apiUrl: apiUrl,
    $el: $(el),
    params: {},
    columnsDef: columnsDef,
    orderBy: '',
    orderDir: 'asc',
    pageSize: pageSize,
    page: 1,
  }
}

async function createDataTable(el, apiUrl, { renders, pageSize }) {
  let table = await getTableDef(el, apiUrl, renders, pageSize);
  table.searchBy = (colName, value) => {
    let param;
    if (colName == null) {
      param = 'search';
    } else {
      param = `columns[${colName}][search]`;
    }
    table.params[param] = value;
    table.page = 1;
    builTableHtml(table);
  }

  table.sortBy = (orderBy, orderDir) => {
    table.orderBy = orderBy;
    table.orderDir = orderDir;
    table.page = 1;
    builTableHtml(table);
  }
  
  table.updateField = (rowIndex, colName, value) => {
    let row = table.rows[rowIndex];
    let pk = row.pk ?? row.id;
   
    $_post(apiUrl, {pk, colName, value}).then(resp => {
      if(resp.ok) {
        builTableHtml(table);
      }else{
        alert('Lỗi xảy ra khi cập nhật dữ liệu');
      }
    });
  }

  table.reload = () => {
    table.params = {};
    table.page = 1;
    table.pageSize = pageSize;
    table.orderBy = '';
    table.orderDir = 'asc';
    builTableHtml(table);
  }

  table.setPage = function (page) {
    table.page = new Number(page) || 1;
    builTableHtml(table);
  };

  table.setPageSize = function(pageSize) {
    table.pageSize = pageSize;
    table.page = 1;
    builTableHtml(table);
  }

  builTableHtml(table);

  return table;
}

function getAsyncSearchConfig({url, placeholder, displayFunc, detailFunc, searchParamsFunc}) {
  return {
    allowClear: true,
    ajax: {
      url: url,
      dataType: 'json',
      delay: 250,
      data: (params) => ({
        term: params.term,
        ...(searchParamsFunc? searchParamsFunc() : {}),
      }),
    },
    placeholder: placeholder || 'Nhập ít nhất một kí tự để tìm kiếm',
    minimumInputLength: 1,
    templateResult: (item) => {
      if (item.loading) {
        return item.text;
      }
      return detailFunc? detailFunc(item) : displayFunc(item);
    },
    templateSelection: (item) => displayFunc(item) || item.text,
  };    
}

$(document).ready(function () {
  $('.table-form input, .table-form textarea, .table-form select').each(function () {
    $(this).addClass('form-control');
  });

  $('.table-form input[type=file]').each(function () {
    $(this).removeClass('form-control');
    $(this).addClass('form-control-file');
  });

  $('.table-form input[type=checkbox]').each(function () {
    $(this).removeClass('form-control');
  });

  $.fn.asyncSelect = function(params) {
    let {onChange} = params;
    
    this.select2(getAsyncSearchConfig(params));
    if(onChange) {
      this.change(function() {
        onChange($(this).val());
      });
    }
  };

  updateDatePicker();
});