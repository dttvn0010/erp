from core.constants import TextEnum
from django.utils.translation import gettext as _

class OrderType(TextEnum):
    SALE = _('sales.order.type.sale')
    DISCOUNT = _('sales.order.type.discount')
    RETURN = _('sales.order.type.return')

class OrderStatus(TextEnum):
    DRAFT = _('sales.order.status.draft')
    PENDING = _('sales.order.status.pending')
    READY_FOR_DELIVERY = _('sales.order.status.ready.for.delivery')
    SHIPPED = _('sales.order.status.shipped')
    CONFIRMED = _('sales.order.status.confirmed')
    CANCELED = _('sales.order.status.canceled')
    RETURNED = _('sales.order.status.returned')