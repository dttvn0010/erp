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

import { NAME_SPACE } from 'redux/reducers/manufacturing/productionProcess/formReducer';

const itemName = 'lệnh SX';
const baseUrl = '/mfr/production-process';

function DeviceUsesModal(){
  let [data, deviceUses, editStepIndex,  showModal, deviceUseErrors] = useSliceSelector(NAME_SPACE, 
        ['data', 'deviceUses', 'editStepIndex', 'showModal', 'deviceUseErrors']);
  
  deviceUses = deviceUses || [];
  deviceUseErrors = deviceUseErrors || [];
  const step = (data.steps || [])[editStepIndex];
  const workflow_step = step?.workflow_step;
  
  const store = useSliceStore(NAME_SPACE);
  const handleClose = () => store.setState({showModal: false});
  
  const handleSave = () => {
    let {data, deviceUses, editStepIndex} = store.getState();
    deviceUses = deviceUses || [];

    const errors = deviceUses.map(deviceUse => {
      let deviceUseError = {};
      if(!deviceUse.device){
        deviceUseError.device = ['Trường này là bắt buộc'];
      }
      return deviceUseError;
    });
    
    const hasError = errors.find(x => x.device);
    
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

  const changeDevice = (index, val) => {
    let {deviceUses} = store.getState();
    deviceUses = copyArray(deviceUses) || [];

    deviceUses[index] = {
      ...deviceUses[index], 
      device_obj: val,
      device: val?.id
    };

    store.setState({deviceUses});
  }

  const changeDeviceClass = (index, val) => {
    let {deviceUses} = store.getState();
    deviceUses = copyArray(deviceUses) || [];
    
    deviceUses[index] = {
      ...deviceUses[index], 
      device_class_obj: val,
      device_class: val?.id,
      device: null,
      device_obj: null
    };
   
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
                <th style={{width: "47%"}}>
                  <a className="ms-3" href='#/' onClick={() => addDeviceUse()}>
                    <i className="fas fa-plus"></i>
                  </a> {" "}
                  Lớp thiết bị
                </th>
                <th style={{width: "47%"}}>Thiết bị</th>
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
                      onChange={val => changeDeviceClass(index, val)}
                      optionsUrl={`${baseUrl}/search-device-class`}
                      getParams={() => ({workflow_step_id: workflow_step})}
                    />
                  </td>
                  <td>
                    <Input
                      type="async-select"
                      key={deviceUse.device_class}
                      value={deviceUse.device_obj}
                      onChange={val => changeDevice(index, val)}
                      optionsUrl={`${baseUrl}/search-device`}
                      getParams={() => ({
                        workflow_step_id: workflow_step, 
                        device_class_id: deviceUse.device_class
                      })}
                    />
                    <ErrorList errors={deviceUseErrors?.[index]?.device}/>
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

export default function ProductionProcessForm({id, update, readOnly}){
  const backUrl = (update || readOnly)? '../' : '../productionProcess';
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

  const changeProduct = (val) => {
    const data = store.getState().data ?? {};
    store.setState({
      data: {
        ...data,
        product: val?.id,
        product_obj: val,
        bom: null,
        bom_obj: null,
        workflow: null,
        workflow_obj: null,
        steps: []
      }
    });
  }

  const changeBom = (val) => {
    const data = store.getState().data ?? {};
    store.setState({
      data: {
        ...data,
        bom: val?.id,
        bom_obj: val,
        workflow: null,
        workflow_obj: null,
        steps:[]
      }
    });
  }

  const changeWorkflow = (val) => {
    if(val.id) {
      axios.get(`/mfr/production-workflow/crud/${val.id}`).then(result => {
        let steps = result.data.steps || [];
        
        steps = steps.map(step => ({
          workflow_step: step.id,
          workflow_step_obj: {id: step.id, name: step.name},
          device_uses: []
        }));

        store.setState({
          data: {
            ...data,
            workflow: val?.id,
            workflow_obj: val,
            steps
          }
        })
      });
    }else {
      store.setState({
        data: {
          ...data,
          workflow: null,
          workflow_obj: null,
          steps: []
        }
      })
    }
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

  
  const saveProductionProcess = async (e) => {
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

  if(loading) {
    return(
      <div className="text-center p-3">
        <Spiner/>
      </div>
    )
  }

  return (
    <>
      <Card
        title={title}
        body={
          <form id="fmt" onSubmit={saveProductionProcess}>
            <div className="row">
              <div className="col-4 form-group">
                <label className="form-label text-bold">Sản phẩm:</label>
                <Input 
                  type="async-select"
                  value={data.product_obj}
                  onChange={changeProduct}
                  readOnly={readOnly}
                  optionsUrl={`${baseUrl}/search-product`}
                />
              </div>
              <div className="col-4 form-group">
                <label className="form-label text-bold">Định lượng NVL:</label>
                <Input 
                  type="async-select"
                  key={data.product}
                  value={data.bom_obj}
                  onChange={changeBom}
                  readOnly={readOnly}
                  optionsUrl={`${baseUrl}/search-product-bom`}
                  getParams={() => ({product_id: data.product})}
                />
                <ErrorList errors={errors.bom}/>
              </div>
              <div className="col-4 form-group">
                <label className="form-label text-bold">Quy trình SX:</label>
                <Input
                  type="async-select"
                  key={data.bom}
                  value={data.workflow_obj}
                  onChange={changeWorkflow}
                  readOnly={readOnly}
                  optionsUrl={`${baseUrl}/search-production-workflow`}
                  getParams={() => ({bom_id: data.bom})}
                />
                <ErrorList errors={errors.workflow}/>
              </div>
            </div>

            <div className="row mt-3">
              <div className="col-4 form-group">
                <label className="form-label text-bold">Số lượng SX:</label>
                <Input 
                  type="number"
                  value={data.product_qty}
                  onChange={val => updateData({product_qty: val})}
                  readOnly={readOnly}
                />
                <ErrorList errors={errors.product_qty}/>
              </div>

              <div className="col-4 form-group">
                <label className="form-label text-bold">Thời gian bắt đầu:</label>
                <Input 
                  type="datetime"
                  value={data.planned_start_date}
                  onChange={val => updateData({planned_start_date: val})}
                  readOnly={readOnly}
                />
                <ErrorList errors={errors.planned_start_date}/>
              </div>

              <div className="col-4 form-group">
                <label className="form-label text-bold">Thời gian kết thúc:</label>
                <Input 
                  type="datetime"
                  value={data.planned_end_date}
                  onChange={val => updateData({planned_end_date: val})}
                  readOnly={readOnly}
                />
                <ErrorList errors={errors.planned_end_date}/>
              </div>
            </div>

            <table className="table mt-3">
              <thead>
                <tr>
                  <th style={{width: "30%"}}>Công đoạn</th>
                  <th style={{width: "20%"}}>Thời gian bắt đầu</th>
                  <th style={{width: "20%"}}>Thời gian kết thúc</th>
                  <th style={{width: "30%"}}>Thiết bị sử dụng</th>
                </tr>
              </thead>
              <tbody>
                {steps.length === 0 &&
                  <tr>
                    <td colSpan="4">
                      Không có công đoạn nào
                    </td>
                  </tr>
                }
                {steps.map((step, index) => 
                  <tr key={index}>
                    <td>
                      <span>{step?.workflow_step_obj?.name}</span>
                    </td>

                    <td>
                      <Input
                        type="datetime"
                        readOnly={readOnly}
                        value={step.planned_start_date}
                        onChange={val => updateStep(index, {planned_start_date: val})}
                      />
                      <ErrorList errors={errors?.steps?.[index]?.planned_start_date}/>
                    </td>

                    <td>
                      <Input
                        type="datetime"
                        readOnly={readOnly}
                        value={step.planned_end_date}
                        onChange={val => updateStep(index, {planned_end_date: val})}
                      />
                      <ErrorList errors={errors?.steps?.[index]?.planned_end_date}/>
                    </td>

                    <td>
                      <div className="d-flex pt-1">
                        {!readOnly &&
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
                          {(step.device_uses || []).map(x => x.device_obj?.name).join(', ')}
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