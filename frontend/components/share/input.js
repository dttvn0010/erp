import { useState, useEffect } from 'react';
import Select from 'react-select';
import AsyncSelect from 'react-select/async';
import DatePicker from "react-datepicker";

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
        onChange={e => onChange(e.target.value)}
        value={value??''}
        {...remainProps}
      />
    )
  }

  if(type === 'textarea') {
    const {value, ...remainProps} = otherProps;
    return (
      <textarea 
        className={"form-control " + className ?? ""}
        onChange={e => onChange(e.target.value)}
        value={value??''}
        {...remainProps}
      ></textarea>
    )
  }

  if(type === 'date') {
    const {dateFormat, ...remainProps} = otherProps;
    return (
      <DatePicker
        className={"form-control " + className ?? ""}
        onChange={onChange}
        dateFormat={dateFormat || "dd/MM/yyyy"}
        {...remainProps}
      />
    )
  }

  if(type === 'datetime') {
    const {dateFormat, timeInputLabel, ...remainProps} = otherProps;
    return (
      <DatePicker
        className={"form-control " + className ?? ""}
        onChange={onChange}
        timeInputLabel={timeInputLabel || "Time:"}
        dateFormat={dateFormat || "dd/MM/yyyy HH:mm"}
        showTimeInput
        {...remainProps}
      />
    )
  }

  if(type === 'select') {
    const {
      optionsUrl, 
      valueField, 
      labelField,
      labelDisplayFunc,
      placeholder,
      ...remainProps
    } = otherProps;

    return (
      <Select 
        options={options}
        className={className}
        onChange={onChange}
        placeholder={placeholder??''}
        {...remainProps}
      />
    )
  }

  if(type === 'async-select') {
    const {
      optionsUrl,
      placeholder,
      valueField,
      labelField,
      labelDisplayFunc,
      ...remainProps
    } =  otherProps;

    return (
      <AsyncSelect 
        className={className}
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