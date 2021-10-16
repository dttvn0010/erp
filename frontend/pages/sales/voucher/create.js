import { getDefaultLayOut } from "utils/helper";
import VoucherForm from "components/sales/voucher/form";

export default function CreateVoucher() {
  return (
    <VoucherForm/>
  );
}

CreateVoucher.getLayout = getDefaultLayOut;