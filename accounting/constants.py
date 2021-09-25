from core.constants import TextEnum
from django.utils.translation import gettext as _

class ExpenseStatus(TextEnum):
    DRAFT = _('expense.status.draft')
    PENDING = _('expense.status.pending')
    APPROVED = _('expense.status.approved')
    CANCELED = _('expense.status.canceled')

class InvoiceType(TextEnum):
    PURCHASE = _('invoice.type.purchase')
    SALE_ORDER = _('invoice.type.sale.order')
    POS_SALE_ORDER = _('invoice.type.pos.sale.order')
    EXPENSE = _('invoice.type.expense')
    OTHER = _('invoice.type.other')