from core.constants import TextEnum
from django.utils.translation import gettext as _

class ExpenseStatus(TextEnum):
    DRAFT = _('expense.status.draft')
    PENDING = _('expense.status.pending')
    APPROVED = _('expense.status.approved')
    CANCELED = _('expense.status.canceled')

class BusinessType(TextEnum):
    PURCHASE = _('business.type.purchase')
    PURCHASE_RETURN = _('business.type.purchase.return')
    PURCHASE_DISCOUNT = _('business.type.purchase.discount')
    SALES = _('business.type.sales')
    SALES_RETURN = _('business.type.sales.return')
    SALES_DISCOUNT = _('business.type.sales.discount')
    POS = _('business.type.pos')
    POS_RETURN = _('business.type.pos.return')
    POS_DISCOUNT = _('business.type.pos.discount')
    EXPENSE = _('business.type.expense')
    INCOME = _('business.type.income')
    OTHER = _('business.type.other')

class BankAccountType(TextEnum):
    INTERNAL = _('bank.account.type.internal')
    PARTNER = _('bank.account.type.partner')
    EMPLOYEE = _('bank.account.type.employee')
