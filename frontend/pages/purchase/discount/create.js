import { getDefaultLayOut } from "utils/helper";
import DiscountForm from "components/purchase/discount/form";

export default function CreateDiscount() {
  return (
    <DiscountForm/>
  );
}

CreateDiscount.getLayout = getDefaultLayOut;