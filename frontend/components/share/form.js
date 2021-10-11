
import axios from 'axios';
import { useEffect, useState } from 'react';
import Select from 'react-select';
import AsyncSelect from 'react-select/async';
import DatePicker from "react-datepicker";
import ErrorList from 'components/share/errorlist';

import {
  getLoadOptions, 
  getOptions, 
  IconButton, 
  IconLink,
  Spiner
} from 'utils/helper';

export function createForm(formMeta, update, id, readOnly){
  let formFields = [];
  let form = {};

  formMeta.fields.forEach(field => {
    let formField = {
      name: field.name,
      Label: () => <label htmlFor={field.name}>{field.label}:</label>,
      Input: ({itemVar}) => {
        
        const [options, setOptions] = useState([]);
        
        useEffect(() => {
          if(field.type === 'select') {
            getOptions({
              url: field.options.url,
              labelField: field.options.labelField,
              valueField: field.options.valueField ?? 'id'
            }).then(options => setOptions(options));
          }
        }, []);


        if(readOnly) {
          if(field.type !== 'textarea') {
            return (
              <input 
                readOnly={true}
                className="form-control" 
                value={itemVar[field.name]} 
                {...field.attrs}
              />
            )
          }else{
            return (
              <textarea 
                readOnly={true}
                className="form-control" 
                value={itemVar[field.name]} 
                {...field.attrs}
              ></textarea>
            )
          }
        }

        if(field.type === 'checkbox') {
          return(
            <input 
              name={field.name} 
              type="checkbox"
              defaultChecked={itemVar[field.name]} 
              {...field.attrs}
            />
          )
        }

        if(field.type === 'input' || field.type === 'number') {
          return (
            <input 
              name={field.name} 
              type={field.type === 'number'? 'number' : 'text'}
              className="form-control" 
              placeholder={field.placeholder}
              defaultValue={itemVar[field.name]} 
              {...field.attrs}
            />
          )
        }

        if(field.type === 'textarea') {
          return (
            <textarea 
              name={field.name} 
              className="form-control" 
              placeholder={field.placeholder}
              defaultValue={itemVar[field.name]} 
              {...field.attrs}
            ></textarea>
          )
        }

        if(field.type === 'date') {
          return (
            <DatePicker
              name={field.name} 
              className="form-control"
              placeholder={field.placeholder}
              defaultValue={itemVar[field.name]}
              dateFormat={field.dateFormat || "dd/MM/yyyy"}
            />
          )
        }

        if(field.type === 'datetime') {
          return (
            <DatePicker
              name={field.name} 
              className="form-control"
              placeholder={field.placeholder}
              defaultValue={itemVar[field.name]}
              timeInputLabel={field.timeInputLabel || "Time:"}
              dateFormat={field.dateFormat || "dd/MM/yyyy HH:mm"}
              showTimeInput
            />
          )
        }

        if(field.type === 'select') {
          return (
            <Select 
              key={itemVar.id}
              name={field.name} 
              options={options}
              placeholder={field.placeholder??''}
              defaultValue={{
                value: itemVar[field.name],
                label: itemVar[field.displayField]
              }}
            />
          )
        }

        if(field.type === 'async-select') {
          return (
            <AsyncSelect 
              key={itemVar.id}
              name={field.name} 
              cacheOptions
              loadOptions={
                getLoadOptions({
                  url: field.options.url,
                  labelField: field.options.labelField, 
                  valueField: field.options.valueField ?? 'id'
                })
              }
              defaultOptions
              isClearable={true}
              placeholder={field.placeholder??''}
              defaultValue={{
                value: itemVar[field.name],
                label: itemVar[field.displayField]
              }}
              noOptionsMessage={() => 'Không tìm thấy kết quả nào'}
              loadingMessage={() => 'Đang tìm kiếm...'} 
            />
          )
        }

        return <></>;
      }
    };

    form[field.name[0].toUpperCase() + field.name.slice(1)] = formField;
    formFields.push(formField);
  });

  return {
    ...form,
    All: ({onSaveSuccess, headerWidth, footer, backUrl, editUrl}) =>{
      const [itemVar, setItemVar] = useState({});
      const [errors, setErrors] = useState({});
      
      useEffect(() => {
        if(id){
          const detailUrl = formMeta.detailUrl.replace('[$id$]', id);
          axios.get(detailUrl).then(result => {
            setItemVar(result.data);
          });
        }
      }, [id]);

      const saveItem = async (e) => {
        e.preventDefault();
        if(readOnly) return;

        const data = new FormData(document.getElementById(formMeta.formId));
        const updateUrl = formMeta.updateUrl.replace('[$id$]', id);
        const createUrl = formMeta.createUrl;

        try{
          const result = await axios({
            method: update? 'put' : 'post',
            url: update? updateUrl : createUrl,
            data:data
          });
          if(onSaveSuccess) onSaveSuccess(result.data);
        }catch(err){
          setErrors(err?.response?.data || {});
          alert('Đã có lỗi xảy ra');
        }
      }

      const loading = (update || readOnly) && !itemVar.id;

      return ( 
        <form id={formMeta.formId} onSubmit={saveItem}>
          <table className="table">
            <tbody>
              {loading &&
                <tr>
                  <td className="text-center">
                    <Spiner/>
                  </td>
                </tr>
              }

              {!loading && formFields.map((formField, i) =>
                <tr key={i}>
                  <th style={{width: headerWidth}}><formField.Label/></th>
                  <td>
                    <formField.Input itemVar={itemVar}/>
                    <ErrorList errors={errors[formField.name]}/>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
          {footer}
          {!footer &&
            <div>
              <IconLink 
                icon="arrow-left"
                variant="secondary"
                href={backUrl}
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
              {readOnly && editUrl &&
                <IconLink
                  href={editUrl}
                  icon="edit"
                  title="Cập nhật"
                />
              }
            </div>
          }
        </form>
      )
    }
  }
}
