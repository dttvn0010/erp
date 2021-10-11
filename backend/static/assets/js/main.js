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

function $_request(url, method, data) {
  var headers = {'X-CSRFToken': getCookie('csrftoken')};

  if (data instanceof FormData) {
    return fetch(url, { method, body: data, headers });
  } else {
    headers['Content-Type'] = 'application/json';
    return fetch(url, { method, body: JSON.stringify(data), headers });
  }
}

function $_post(url, data){
  return $_request(url, 'POST', data);
}

function $_put(url, data){
  return $_request(url, 'PUT', data);
}

function $_delete(url, data){
  return $_request(url, 'DELETE', data);
}
function serializeForm(fmt) {
  let formData = new FormData(fmt);
  let data = {};
  for(let pair of formData.entries()) {
    data[pair[0]] = pair[1]
  }
  return data;
}

function formatThousand(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

// ===== Data table
const PAGE_SIZE = 10;

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
                `<span id="filter-${col.data}" class="filter ${table.searchParams[col.data]?'active':''}">
                  <span data-bs-toggle="dropdown"><i class="fas fa-filter" ></i></span> 
                  <div class="dropdown-menu inline-editor p-1">
                    
                    ${col.dtype == 'text'?
                      `<div class="full-width dropdown-keep-open">
                        <label class="mb-1">Nhập giá trị để tìm:</label>
                        <input type="text" class="full-width" value="${table.searchParams[col.data]??''}"/>
                        <button class="mt-1 btn btn-sm btn-success btn-filter btn-filter-text" data-col='${col.data}'>
                          <i class="fas fa-check"></i>
                        </button>
                      </div>`: ''
                    }

                    ${col.dtype == 'number'?
                      `<div class="full-width dropdown-keep-open">
                        <label class="mb-1">Nhập giá trị để tìm:</label>
                        <input type="number" class="full-width" value="${table.searchParams[col.data]??''}"/>
                        <button class="mt-1 btn btn-sm btn-success btn-filter btn-filter-text" data-col='${col.data}'>
                          <i class="fas fa-check"></i>
                        </button>
                      </div>`: ''
                    }

                    ${col.dtype == 'bool'?
                      `<div class="full-width dropdown-keep-open p-2">
                        <div class="radio-group">
                          <div class="mb-2">
                            <input type="radio" value="" ${(table.searchParams[col.data]??'')==''? 'checked':''} 
                              name="input-filter-${col.data}">

                            <label>Tất cả</label>
                          </div>
                          <div class="mb-2">
                            <input type="radio" value="1" ${(table.searchParams[col.data]??'')=='1'? 'checked':''} 
                              name="input-filter-${col.data}">

                            <label>Có</label>
                          </div>
                          <div class="mb-2">
                            <input type="radio" value="0" ${(table.searchParams[col.data]??'')=='0'? 'checked':''}
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
                        <div class="d-flex">
                          <div class="half-width px-1">
                            <label class="mb-1">Từ ngày:</label>
                            <input class="full-width" type="text" value="${(table.searchParams[col.data]??'--').split('--')[0]}" />
                          </div>

                          <div class="half-width px-1">
                            <label class="mb-1">Đến ngày:</label>
                            <input class="full-width" type="text" value="${(table.searchParams[col.data]??'--').split('--')[1]}" />
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
                        
                        ${!col.asyncSearch? `
                          <select multiple class="full-width dropdown-keep-open">
                            ${col.displayList.map(item =>( 
                              `<option value="${item[0]}"
                                ${(table.searchParams[col.data]??'').split(',').includes((item[0]??'').toString())?'selected':''}
                              >
                                ${item[1]}
                              </option>`)
                            ).join('')}
                          </select>
                        `: ''}

                        ${col.asyncSearch? `
                          <select async data-col=${col.data} multiple class="full-width dropdown-keep-open">
                            ${(table.searchOptions[col.data]||[]).map(item =>( 
                              `<option value="${item[0]}" selected>
                                ${item[1]}
                              </option>`)
                            ).join('')}
                          </select>
                        `: ''}
                        
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

function replaceAll(st, oldTag, newTag) {
  return st.split(oldTag).join(newTag);
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
                          `<textarea rows="10" class="full-width inline-editor-value">${replaceAll(row[col.data]??'', '<br>', '\n')}</textarea>`: ''
                        }

                        ${col.dtype == 'date' ?
                          `<input type="text" class="date-picker full-width inline-editor-value" value="${row[col.data]??''}"/>`: ''
                        }

                        ${col.dtype == 'datetime'?
                          `<input type="text" class="date-time-picker full-width inline-editor-value" value="${row[col.data]??''}"/>`: ''
                        }

                        ${col.dtype == 'category' && !col.asyncSearch  ?
                          `<select class="full-width inline-editor-value">
                            ${col.blank?
                              `<option value>---------</option>`:''
                            }
                            ${!col.editList.map(item => item[0].toString()).includes(row[col.data + '_id'].toString()) ?
                              `<option value="${row[col.data + '_id']}">
                                ${row[col.data]}
                              </option>
                              `: ''
                            }
                            ${col.editList.map(item => 
                              `<option value="${item[0]}" ${item[0]==row[col.data + '_id']?'selected':''}>
                                ${item[1]}
                              </option>`
                            )}
                          </select>`: ''
                        }

                        ${col.dtype == 'category' && col.asyncSearch  ?
                          `<select async data-col=${col.data} class="full-width inline-editor-value">
                            ${col.blank?
                              `<option value>---------</option>`:''
                            }
                            <option value="${row[col.data + '_id']}">
                              ${row[col.data]}
                            </option>
                          </select>`: ''
                        }

                        ${col.dtype == 'multiCategory' && !col.asyncSearch ?
                          `<select class="full-width inline-editor-value" multiple>
                            ${col.displayList.map(item => 
                              `<option value="${item[0]}" ${(row[col.data + '_id']??[]).includes(item[0].toString())?'selected':''}>
                                ${item[1]}
                              </option>`
                            )}
                          </select>`: ''
                        }

                        ${col.dtype == 'multiCategory' && col.asyncSearch ?
                          `<select async data-col=${col.data} class="full-width inline-editor-value" multiple>
                            ${(row[col.data]||[]).map.map((text, index) => 
                              `<option value="${row[col.data + '_id'][index]}" selected>
                                ${text}
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
  pageSize = new Number(pageSize);
  let start = (page - 1) * pageSize;
  const end = Math.min(start + pageSize, total);
  start = Math.min(1+start, total);
  let numPages = Math.ceil(total / pageSize);

  return (
    `<div>
        <span>Hiển thị ${start}-${end} trên tổng số ${total} kết quả</span>
        <div class="float-end d-flex">
          <div class="pe-4">
            <span>Kích thước trang:</span>
            <select class="page-size-select">
              <option ${pageSize==10?'selected':''}>10</option>
              <option ${pageSize==25?'selected':''}>25</option>
              <option ${pageSize==50?'selected':''}>50</option>
              <option ${pageSize==100?'selected':''}>100</option>
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
  let thead = renderTableHead(table);
  let loadingBody = `
    <tbody>
      <tr>
        <td colspan="${table.columnsDef.length}" class="text-center">
          <div class="spinner-border" role="status">
            <span class="sr-only"></span>
          </div>
        </td>
      </tr>
    </tbody>
  `;

  table.$el.html(`
    <table class="table table-bordered data-table">
      ${thead}
      ${loadingBody}
    </table>
  `);

  let apiUrl = table.apiUrl;

  if (!apiUrl.includes('?')) {
    apiUrl += '?'
  }

  for (let colName in table.searchParams) {
    apiUrl += `&columns[${colName}][search]=${encodeURIComponent(table.searchParams[colName])}`;
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

  let resp = await $_get(apiUrl);
  let data = await resp.json();
  let rows = data.data || [];
  let tbody = renderTableBody(table.columnsDef, rows);
  let pagination = renderPagination(table.page, data.total, table.pageSize);

  let html = (
    `
      <button class="btn btn-sm float-end btn-reload"><i class="fas fa-sync" ></i></button>
      <table class="table table-bordered data-table">
        ${thead}
        ${tbody}
      </table>
      ${pagination}`
  );

  table.$el.html(html);
  table.rows = rows;

  table.$el.find('.btn-reload').click(function() {
    table.reload();
  });
  
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
        let ids = select.val();
        let selectedOptions = [];

        table.$el.find(`#filter-${colName} .select2-selection__choice__display`).each(function(){
          selectedOptions.push([ids[selectedOptions.length], $(this).html().trim()]);
        });

        table.searchOptions[colName] = selectedOptions;
        
        table.searchBy(colName, ids.join(','));
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

  //table.$el.find('.date-picker').datetimepicker({format: 'DD/MM/yyyy'});

  //table.$el.find('.date-time-picker').datetimepicker({format: 'DD/MM/yyyy HH:mm:ss'});

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

  if(table.onLoad){
    table.onLoad(table);
  }
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
    searchParams: {},
    searchOptions: {},
    columnsDef: columnsDef,
    orderBy: '',
    orderDir: 'asc',
    pageSize: pageSize,
    page: 1,
  }
}

async function createDataTable(el, apiUrl, { renders, pageSize, onLoad }) {
  pageSize = pageSize || PAGE_SIZE;
  let table = await getTableDef(el, apiUrl, renders, pageSize);
  table.onLoad = onLoad;
  table.searchBy = (colName, value) => {
    table.searchParams[colName] = value;
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
    table.searchParams = {};
    table.searchOptions = {};
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

function getAsyncSearchConfig({url, placeholder, initialData, displayFunc, detailFunc, searchParamsFunc}) {
  return {
    allowClear: true,
    data: initialData,
    ajax: {
      url: url,
      dataType: 'json',
      delay: 250,
      data: (params) => ({
        term: params.term,
        ...(searchParamsFunc? searchParamsFunc() : {}),
      }),
    },
    placeholder: placeholder || '',
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

async function handleErrorResponse(resp) {
  $(window).scrollTop(0);

  try{
    let errors = await resp.json();

    for(let [key, value] of Object.entries(errors)) {
      if(Array.isArray(value)){
        let html = value.map(e => `<li>${e}</li>`).join('');
        $(`.errorlist[data-for=${key}]`).html(html);
      }else{
        for(let [subkey, subvalue] of Object.entries(value)) {
          let html = subvalue.map(e => `<li>${e}</li>`).join('');
          $(`.errorlist[data-for="${key}.${subkey}"]`).html(html);
        }
      }
    }
  }catch {
    alert('Lỗi xảy ra');
  }
}

$(document).ready(function () {
  $('.table-form input, .table-form textarea, .table-form select').addClass('form-control');
  $('.table-form input[type=checkbox], .table-form input[type=radio]').removeClass('form-control');
  $('.select2-search__field').removeClass('form-control');

  $('.table-form input[type=file]').removeClass('form-control');
  $('.table-form input[type=file]').addClass('form-control-file');

  $.fn.asyncSelect = function(params) {
    let {onChange} = params;
    
    this.select2(getAsyncSearchConfig(params));

    if(onChange) {
      this.change(function() {
        let data = $(this).select2('data');
        if(data.length == 0) {
          $(this).val(null);
        }
        onChange($(this), data);
      });
    }
  };

  updateDatePicker();
});