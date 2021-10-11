import { getDefaultLayOut } from "utils/helper";
import OrderForm from "components/purchase/order/form";

export default function CreateOrder() {
  return (
    <OrderForm/>
  );
}

CreateOrder.getLayout = getDefaultLayOut;