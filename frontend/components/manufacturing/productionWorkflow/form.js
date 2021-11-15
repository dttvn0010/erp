import axios from 'axios';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import { Modal, Button } from 'react-bootstrap';

import Card from 'components/share/card';
import Input from 'components/share/input';
import ErrorList from 'components/share/errorlist';

import { 
  IconLink, 
  IconButton,
  Spiner,
  useSliceStore,
  useSliceSelector,
  copyArray
} from 'utils/helper';

import { NAME_SPACE } from 'redux/reducers/manufacturing/productionWorkflow/formReducer';

const itemName = 'quy trình SX';
const baseUrl = '/mfr/production-workflow';

function DeviceUsesModal(){
  let [deviceUses,   showModal, deviceUseErrors] = useSliceSelector(NAME_SPACE, 
        ['deviceUses', 'showModal', 'deviceUseErrors']);
  
  deviceUses = deviceUses || [];
  deviceUseErrors = deviceUseErrors || [];

  const store = useSliceStore(NAME_SPACE);
  const handleClose = () => store.setState({showModal: false});
  
  const handleSave = () => {
    let {data, deviceUses, editStepIndex} = store.getState();
    deviceUses = deviceUses || [];

    const errors = deviceUses.map(deviceUse => {
      let deviceUseError = {};
      if(!deviceUse.device_class) {
        deviceUseError.device_class = ['Trường này là bắt buộc'];
      }
      if(!deviceUse.hour_per_unit){
        deviceUseError.hour_per_unit = ['Trường này là bắt buộc'];
      }
      return deviceUseError;
    });
    
    const hasError = errors.find(x => x.device_class || x.hour_per_unit);
    
    if(hasError) {
      store.setState({deviceUseErrors: errors});
    }else {
      const steps = copyArray(data.steps) || [];
      steps[editStepIndex].device_uses = deviceUses;
      store.setState({
        deviceUseErrors: null,
        data: {...data, steps},
        showModal: false
      });
    }
  }

  const addDeviceUse = () => {
    let {deviceUses} = store.getState();
    deviceUses = deviceUses || [];
    deviceUses = [...deviceUses, {}]
    store.setState({deviceUses});
  }

  const updateDeviceUse = (index, data) => {
    for(let [k,v] of Object.entries(data)) {
      if(k.endsWith('_obj')) data[k.replace('_obj', '')] = v?.id;
    }

    let {deviceUses} = store.getState();
    deviceUses = copyArray(deviceUses) || [];
    deviceUses[index] = {...deviceUses[index], ...data};
    store.setState({deviceUses});
  }

  const deleteDeviceUse = (index) => {
    let {deviceUses} = store.getState();
    deviceUses = copyArray(deviceUses) || [];
    deviceUses.splice(index, 1);
    store.setState({deviceUses});
  }

  return(
    <Modal size="lg" show={showModal} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Danh sách thiết bị sử dụng</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <form id="fmt">
          <table className="table">
            <thead>
              <tr>
                <th style={{width: "60%"}}>
                  <a className="ms-3" href='#/' onClick={() => addDeviceUse()}>
                    <i className="fas fa-plus"></i>
                  </a> Thiết bị
                </th>
                <th>Số giờ sử dụng/1 sản phẩm</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {deviceUses.length === 0 &&
                <tr>
                  <td colSpan="3">
                    Chưa có thiết bị
                  </td>
                </tr>
              }
              {deviceUses.map((deviceUse, index) => 
                <tr key={index}>
                  <td>
                    <Input
                      type="async-select"
                      value={deviceUse.device_class_obj}
                      optionsUrl={`${baseUrl}/search-device-class`}
                      onChange={val => updateDeviceUse(index, {device_class_obj: val})}
                    />
                    <ErrorList errors={deviceUseErrors?.[index]?.device_class}/>
                  </td>
                  <td>
                    <Input
                      type="number"
                      value={deviceUse.hour_per_unit}
                      onChange={val => updateDeviceUse(index, {hour_per_unit: val})}
                    />
                    <ErrorList errors={deviceUseErrors?.[index]?.hour_per_unit}/>
                  </td>
                  <td>
                    <a className="me-2" href='#/' onClick={() => deleteDeviceUse(index)}>
                      <i className="fas fa-trash text-danger"></i>
                    </a>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
          <div className="float-end">
            <Button size="sm" variant="secondary" onClick={handleClose}>
            Đóng lại
            </Button>
            <Button size="sm" className="ms-1" variant="primary" onClick={handleSave}>
              Lưu lại
            </Button>
          </div>
        </form>
      </Modal.Body>
    </Modal>
  )
}

export default function ProductionWorkflowForm({id, update, readOnly}){
  const backUrl = (update || readOnly)? '../' : '../productionWorkflow';
  const editUrl = id? `../update/${id}` : null;
  
  const router = useRouter();
  const store = useSliceStore(NAME_SPACE);
  const [data, errors] = useSliceSelector(NAME_SPACE, ['data', 'errors']);
  const steps = data.steps || [];

  useEffect(() => {
    store.setState({
      data: {},
      errors: {}
    });

    if(id) {
      axios.get(`${baseUrl}/crud/${id}`).then(result => {
        store.setState({data: result.data});
      });
    }
  }, [id]);

  const updateData = newData => {
    const data = store.getState().data ?? {};
    
    for(let [k,v] of Object.entries(newData)) {
      if(k.endsWith('_obj')) newData[k.replace('_obj', '')] = v?.id;
    }

    store.setState({
      data: {
        ...data,
        ...newData
      }
    }) 
  }

  const addStep = (index) => {
    const {data} = store.getState();
    const steps = copyArray(data.steps) || [];
  
    if(index == -1) {
      steps.push({});
    }else{
      steps.splice(index+1, 0, {});
    }
    
    store.setState({data: {...data, steps}});
  }

  const updateStep = (index, stepData) => {
    for(let [k,v] of Object.entries(stepData)) {
      if(k.endsWith('_obj')) stepData[k.replace('_obj', '')] = v?.id;
    }

    const {data} = store.getState();
    const steps = copyArray(data.steps) || [];
    steps[index] = {...steps[index], ...stepData};
    store.setState({data: {...data, steps}});
  }

  const deleteStep = (index) => {
    const {data} = store.getState();
    const steps = copyArray(data.steps) || [];
    steps.splice(index, 1);
    store.setState({data: {...data, steps}});
  }

  const saveProductionWorkflow = async (e) => {
    e.preventDefault();
    if(readOnly) return; 

    const {data} = store.getState();

    try{
      if(update) {
        await axios.put(`${baseUrl}/crud/${id}/`, data);
      }else{
        await axios.post(`${baseUrl}/crud/`, data);
      }

      router.push(backUrl);
    }catch(err){
      store.setState({
        errors: err?.response?.data ?? {}
      });
      console.log(err?.response?.data );
      alert('Đã có lỗi xảy ra');
    }
  }

  const editDeviceUses = (index) => {
    const {data} = store.getState();

    store.setState({
      showModal: true,
      deviceUses: data?.steps?.[index].device_uses,
      deviceUseErrors: null,
      editStepIndex: index,
    });
  }

  const title = (
    readOnly? `Xem ${itemName}` : (update? `Cập nhập ${itemName}` : `Thêm ${itemName}`)
  );
  
  const loading = (update || readOnly) && !data.id;
  const activeReadonly = readOnly || data?.status === 'ACTIVE';

  if(loading) {
    return(
      <div className="text-center p-3">
        <Spiner/>
      </div>
    )
  }

  let ncol = 4;
  if(activeReadonly) ncol -= 1;

  return (
    <>
      <Card
        title={title}
        body={
          <form id="fmt" onSubmit={saveProductionWorkflow}>
            <div className="row">
              <div className="col-6 form-group">
                <label className="form-label text-bold">Tên quy trình SX:</label>
                <Input 
                  type="input"
                  value={data.name}
                  onChange={val => updateData({name: val})}
                  readOnly={readOnly}
                />
                <ErrorList errors={errors.name}/>
              </div>
              <div className="col-6 form-group">
                <label className="form-label text-bold">Đinh lượng NVL:</label>
                <Input 
                  type="async-select"
                  value={data.bom_obj}
                  onChange={val => updateData({bom_obj: val})}
                  readOnly={activeReadonly}
                  optionsUrl={`${baseUrl}/search-product-bom`}
                />
                <ErrorList errors={errors.bom}/>
              </div>
            </div>

            <table className="table mt-3">
              <thead>
                <tr>
                  {!activeReadonly &&
                    <th className="text-center">
                      <a className="ms-3" href='#/' onClick={() => addStep(-1)}>
                        <i className="fas fa-plus"></i>
                      </a>
                    </th>
                  }
                  <th style={{width: "30%"}}>Công đoạn</th>
                  <th style={{width: "30%"}}>Phân xưởng</th>
                  <th style={{width: "35%"}}>Thiết bị sử dụng</th>
                </tr>
              </thead>
              <tbody>
                {steps.length === 0 &&
                  <tr>
                    <td colSpan={ncol}>
                      Chưa có công đoạn nào
                    </td>
                  </tr>
                }
                {steps.map((step, index) => 
                  <tr key={index}>
                    {!activeReadonly &&
                      <td>
                        <div className="pt-1">
                          <a className="me-2" href='#/' onClick={() => deleteStep(index)}>
                            <i className="fas fa-trash text-danger"></i>
                          </a>
                          <a href='#/' onClick={() => addStep(index)}>
                            <i className="fas fa-plus"></i>
                          </a>
                        </div>
                      </td>
                    }
                    
                    <td>
                      <Input
                        type="input"
                        readOnly={activeReadonly}
                        value={step.name}
                        onChange={val => updateStep(index, {name: val})}
                      />
                      <ErrorList errors={errors?.steps?.[index]?.name}/>
                    </td>

                    <td>
                      <Input
                        type="async-select"
                        readOnly={activeReadonly}
                        value={step.workcenter_obj}
                        optionsUrl={`${baseUrl}/search-work-center`}
                        onChange={val => updateStep(index, {workcenter_obj: val})}
                      />
                      <ErrorList errors={errors?.steps?.[index]?.workcenter}/>
                    </td>

                    <td>
                      <div className="d-flex pt-1">
                        {!activeReadonly &&
                          <div>
                            <a className="me-2" href='#/' onClick={() => editDeviceUses(index)}>
                              <i className="fas fa-edit"></i>
                            </a>
                          </div>
                        }
                        <div>
                          {(!step.device_uses || step.device_uses.length == 0) &&
                            <span>Chưa có thiết bị</span>
                          }
                          {(step.device_uses || []).map(device_use => device_use.device_class_obj?.name).join(', ')}
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
            <div className="row mt-3">
              <div className="col">
                <div>
                  <IconLink 
                    href={backUrl}
                    icon="arrow-left"
                    variant="secondary"
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
                  {readOnly && 
                    <IconLink
                      href={editUrl}
                      icon="edit"
                      title="Cập nhật"
                    />
                  }
                </div>
              </div>
            </div>
          </form>
        }
      />
      <DeviceUsesModal/>
    </>
  )
}