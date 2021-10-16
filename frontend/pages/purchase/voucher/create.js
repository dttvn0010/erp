import { getDefaultLayOut } from "utils/helper";
import VoucherForm from "components/purchase/voucher/form";

export default function CreateVoucher() {
  return (
    <VoucherForm/>
  );
}

CreateVoucher.getLayout = getDefaultLayOut;