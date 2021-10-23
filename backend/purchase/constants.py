from core.constants import TextEnum
from django.utils.translation import gettext as _

class OrderType(TextEnum):
    PURCHASE = _('purchase.order.type.purchase')
    DISCOUNT = _('purchase.order.type.discount')
    RETURN = _('purchase.order.type.return')

class OrderStatus(TextEnum):
    DRAFT = _('purchase.order.status.draft')
    REQUESTED = _('purchase.order.status.requested')
    APPROVED = _('purchase.order.status.approved')
    ORDERED = _('purchase.order.status.ordered')
    RECEIVED = _('purchase.order.received')
    CANCELED = _('purchase.order.canceled')
    RETURNED = _('purchase.order.returned')