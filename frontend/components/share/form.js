
import axios from 'axios';
import { useEffect, useState } from 'react';
import ErrorList from 'components/share/errorlist';
import Input from 'components/share/input';

import {
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
      
      Input: ({itemVar, updateItemVar}) => {
        
        if(field.type === 'file') {
          return (
            <>
              {!readOnly && <input 
                type='file'
                className="form-control-file" 
                onChange={e => updateItemVar({[field.name + '_file']: e.target.files[0]})}
                {...field.attrs}
              />}
              {itemVar[field.name] && (
                <a target="_blank" href={itemVar[field.name]}>
                  File hiện tại
                </a>
              )}
            </>
          )
        }

        let props = {...field.attrs};
        let field_name = field.name;
        
        if(field.type === 'async-select' || field.type === 'select') {
          const {getParams} = props;
          if(getParams){
            props.getParams = () => {
              return getParams(id, itemVar);
            }
          }
          field_name += '_obj';
        }

        let keys = field.keys ? (
          field.keys.map(key => {
            let key_field = formMeta.fields.find(f => f.name === key);
            if(key_field?.type === 'select' || key_field?.type === 'async-select'){
              return itemVar[`${key}_obj`]?.id;
            }
            return itemVar[key];
          })
        ): null;
        
        const onChange = (val) => {
          let newData = {
            [field_name]: val
          };

          if(field.type === 'async-select' || field.type === 'select') {
            newData[field.name] = val?.id;
          }

          const dependentFields = formMeta.fields.filter(f => (f.keys??[]).includes(field.name));
          
          dependentFields.forEach(f => {
            newData[f.name] = null;
            if(f.type === 'select' || f.type === 'async-select') {
              newData[f.name + '_obj'] = null;
            }
          });

          console.log('newData=', newData);
          updateItemVar(newData);
        }

        return (
          <Input
            key={keys}
            name={field_name}
            type={field.type}
            value={itemVar[field_name]??null}
            onChange={onChange}
            readOnly={readOnly}
            {...props}
          />
        );
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
      
      const updateItemVar = newData => setItemVar({...itemVar, ...newData});

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

        const updateUrl = formMeta.updateUrl.replace('[$id$]', id);
        const createUrl = formMeta.createUrl;
        
        let data = new FormData()
        
        formMeta.fields.forEach(field => {
          if(field.type === 'select' || field.type === 'async-select') {
            const value = itemVar[field.name + '_obj'];
            data.append(field.name, value?.id??'');
          }else if (field.type === 'file'){
            const value = itemVar[field.name + '_file'];
            if(value){
              data.append(field.name, value, value.name);
            }
          }else{
            const value = itemVar[field.name];
            data.append(field.name, value ?? '');
          }
        });

        try{
          const result = await axios({
            method: update? 'put' : 'post',
            url: update? updateUrl : createUrl,
            data: data
          });
          if(onSaveSuccess) onSaveSuccess(result.data);
        }catch(err){
          setErrors(err?.response?.data || {});
          console.log(err?.response?.data);
          alert('Đã có lỗi xảy ra');
        }
      }

      const loading = (update || readOnly) && !itemVar.id;

      return ( 
        <form onSubmit={saveItem} encType="multipart/form-data">
          {itemVar?.bank_obj?.id}
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
                    <formField.Input itemVar={itemVar} updateItemVar={updateItemVar}/>
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
