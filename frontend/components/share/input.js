import { useState, useEffect } from 'react';
import Select from 'react-select';
import AsyncSelect from 'react-select/async';
import DatePicker from "react-datepicker";
import moment from 'moment';

import {
  getLoadOptions, 
  getOptions, 
} from 'utils/helper';


export default function Input(props) {
  let {
    type, 
    value,
    readOnly, 
    className, 
    onChange, 
    placeholder,
    valueField,
    labelField, 
    optionsUrl,
    params,
    getParams,
    optionDisplayFunc,
    resultDisplayFunc,
    dateFormat,
    timeInputLabel,
    ...otherProps
  } = props;

  const [options, setOptions] = useState([]);

  useEffect(() => {
    if(type === 'select') {
      if(optionsUrl){
        getOptions({
          url: optionsUrl ?? '',
          labelField: labelField ?? 'name',
          valueField: valueField ?? 'id',
          params,
          getParams,
        }).then(options => setOptions(options));
      }
    }
  }, []);

  if(readOnly) {
    if(type === 'select' || type === 'async-select') {
      if(resultDisplayFunc) {
        value = resultDisplayFunc(value);
      }else if(optionDisplayFunc){
        value = props.optionDisplayFunc(value);
      }else{
        value = (value||{})[labelField ?? 'name'] ?? (value?.label);
      }
    }

    if(type === 'textarea') {
      return (
        <textarea 
          readOnly={true}
          className={"form-control " + className ?? ""} 
          value={value??''}
          {...otherProps}
        ></textarea>
      )
    }else if(type === 'checkbox') {
      return (
        <input 
          type="checkbox"
          checked={value ?? false} 
          {...otherProps}
        />
      );
    }else{
      return (
        <input 
          readOnly={true}
          className={"form-control " + className ?? ""} 
          value={value??''}
          {...otherProps}
        />
      )
    }
  }

  if(type === 'input' || type === 'number') {
    return (
      <input 
        type={type === 'number'? 'number' : 'text'}
        className={"form-control " + className ?? ""} 
        onChange={onChange? e => onChange(e.target.value) : onChange}
        value={value??''}
        placeholder={placeholder??''}
        {...otherProps}
      />
    )
  }

  if(type === 'checkbox') {
    return (
      <input 
        type="checkbox"
        checked={value ?? false} 
        onChange={onChange? e => onChange(e.target.checked): onChange}
        {...otherProps}
      />
    );
  }

  if(type === 'textarea') {
    return (
      <textarea 
        className={"form-control " + className ?? ""}
        onChange={onChange? e => onChange(e.target.value) : onChange}
        value={value??''}
        placeholder={placeholder??''}
        {...otherProps}
      ></textarea>
    )
  }

  if(type === 'date' || type === 'datetime') {
    dateFormat = dateFormat || (type ==='date'? 'dd/MM/yyyy': 'dd/MM/yyyy HH:mm');
    const momentDateFormat = dateFormat.replace('dd', 'DD');
    
    return (
      <DatePicker
        className={"form-control " + className ?? ""}
        value={value??''}
        onChange={onChange? (val) => onChange(moment(val).format(momentDateFormat)) : onChange}
        timeInputLabel={timeInputLabel || "Time:"}
        dateFormat={dateFormat}
        showTimeInput={type === 'datetime'}
        {...otherProps}
      />
    )
  }

  if(type === 'select') {
    value = {
      ...value,
      value: (value||{})[valueField??'id'],
      label: (value||{})[labelField??'name']
    }
    
    return (
      <Select 
        value={value}
        options={optionsUrl? options : props.options}
        formatOptionLabel={(item, {context}) => {
          if(item.isDisabled) return item.label;
          const label = (optionDisplayFunc)? optionDisplayFunc(item) : item[labelField??'name'];
          if(context === 'value') {
            return (resultDisplayFunc)? resultDisplayFunc(item) : label;
          }else if(context === 'menu') {
            return label;
          }
        }}
        className={className}
        onChange={onChange}
        isClearable={true}
        placeholder={placeholder??''}
        noOptionsMessage={() => 'Không tìm thấy kết quả nào'}
        {...otherProps}
      />
    )
  }

  if(type === 'async-select') {
    value = {
      ...value,
      value: (value||{})[valueField??'id'],
      label: (value||{})[labelField??'name']
    }
    
    return (
      <AsyncSelect 
        className={className}
        value={value??null}
        onChange={onChange}
        cacheOptions
        loadOptions={
          getLoadOptions({
            url: optionsUrl ?? '',
            labelField: labelField ?? 'name', 
            valueField: valueField ?? 'id',
            params,
            getParams,
          })
        }
        formatOptionLabel={(item, {context}) => {
          if(item.isDisabled) return item.label;
          const label = (optionDisplayFunc)? optionDisplayFunc(item) : item[labelField??'name'];
          if(context === 'value') {
            return (resultDisplayFunc)? resultDisplayFunc(item) : label;
          }else if(context === 'menu') {
            return label;
          }
        }}
        defaultOptions
        isClearable={true}
        placeholder={placeholder??''}
        noOptionsMessage={() => 'Không tìm thấy kết quả nào'}
        loadingMessage={() => 'Đang tìm kiếm...'} 
        {...otherProps}
      />
    )
  }
  return <></>;
}