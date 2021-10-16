import { getDefaultLayOut } from "utils/helper";
import DiscountForm from "components/sales/discount/form";

export default function CreateDiscount() {
  return (
    <DiscountForm/>
  );
}

CreateDiscount.getLayout = getDefaultLayOut;