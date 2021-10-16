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
  const {type, readOnly, className, onChange, ...otherProps} = props;
  const [options, setOptions] = useState([]);

  useEffect(() => {
    if(type === 'select') {
      getOptions({
        optionsUrl: props.optionsUrl,
        labelField: props.labelField,
        labelDisplayFunc: props.labelDisplayFunc,
        valueField: props.valueField ?? 'id'
      }).then(options => setOptions(options));
    }
  }, []);

  if(readOnly) {
    let value = props.value || props.defaultValue;
    if(type === 'select' || type === 'async-select') {
      value = value.label;
    }

    if(type !== 'textarea') {
      return (
        <input 
          readOnly={true}
          className={"form-control " + className ?? ""} 
          value={value}
        />
      )
    }else{
      return (
        <textarea 
          readOnly={true}
          className={"form-control " + className ?? ""} 
          value={value}
          rows={props.rows}
        ></textarea>
      )
    }
  }

  if(type === 'input' || type === 'number') {
    const {value, ...remainProps} = otherProps;
    return (
      <input 
        type={type === 'number'? 'number' : 'text'}
        className={"form-control " + className ?? ""} 
        onChange={onChange? e => onChange(e.target.value) : onChange}
        value={value}
        {...remainProps}
      />
    )
  }

  if(type === 'textarea') {
    const {value, ...remainProps} = otherProps;
    return (
      <textarea 
        className={"form-control " + className ?? ""}
        onChange={onChange? e => onChange(e.target.value) : onChange}
        value={value}
        {...remainProps}
      ></textarea>
    )
  }

  if(type === 'date' || type === 'datetime') {
    let {
      dateFormat,
      timeInputLabel, 
      value, 
      defaultValue,
      ...remainProps
    } = otherProps;

    dateFormat = dateFormat || (type ==='date'? 'dd/MM/yyyy': 'dd/MM/yyyy HH:mm');
    const momentDateFormat = dateFormat.replace('dd', 'DD');
    
    return (
      <DatePicker
        className={"form-control " + className ?? ""}
        value={value}
        defaultValue={defaultValue}
        onChange={onChange? (val) => onChange(moment(val).format(momentDateFormat)) : onChange}
        timeInputLabel={timeInputLabel || "Time:"}
        dateFormat={dateFormat}
        showTimeInput={type === 'datetime'}
        {...remainProps}
      />
    )
  }

  if(type === 'select') {
    let {
      optionsUrl, 
      value,
      defaultValue,
      valueField, 
      labelField,
      labelDisplayFunc,
      placeholder,
      ...remainProps
    } = otherProps;

    if(value){
      value = {
        ...value,
        value: value[valueField??'id'],
        label: value[labelField]
      }
    }

    if(defaultValue){
      defaultValue = {
        ...defaultValue,
        value: defaultValue[valueField??'id'],
        label: defaultValue[labelField]
      }
    }

    return (
      <Select 
        value={value}
        defaultValue={defaultValue}
        options={options}
        className={className}
        onChange={onChange}
        placeholder={placeholder??''}
        {...remainProps}
      />
    )
  }

  if(type === 'async-select') {
    let {
      optionsUrl,
      placeholder,
      value,
      defaultValue,
      valueField,
      labelField,
      labelDisplayFunc,
      ...remainProps
    } =  otherProps;

    if(value){
      value = {
        ...value,
        value: value[valueField??'id'],
        label: value[labelField]
      }
    }

    if(defaultValue){
      defaultValue = {
        ...defaultValue,
        value: defaultValue[valueField??'id'],
        label: defaultValue[labelField]
      }
    }

    return (
      <AsyncSelect 
        className={className}
        value={value}
        defaultValue={defaultValue}
        onChange={onChange}
        cacheOptions
        loadOptions={
          getLoadOptions({
            url: optionsUrl,
            labelField: labelField, 
            labelDisplayFunc: labelDisplayFunc,
            valueField: valueField ?? 'id'
          })
        }
        defaultOptions
        isClearable={true}
        placeholder={placeholder??''}
        noOptionsMessage={() => 'Không tìm thấy kết quả nào'}
        loadingMessage={() => 'Đang tìm kiếm...'} 
        {...remainProps}
      />
    )
  }
  return <></>;
}