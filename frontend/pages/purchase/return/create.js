import { getDefaultLayOut } from "utils/helper";
import ReturnForm from "components/purchase/return/form";

export default function CreateReturn() {
  return (
    <ReturnForm/>
  );
}

CreateReturn.getLayout = getDefaultLayOut;