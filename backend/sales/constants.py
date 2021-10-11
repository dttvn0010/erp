from core.constants import TextEnum
from django.utils.translation import gettext as _

class OrderStatus(TextEnum):
    DRAFT = _('sales.order.status.draft')
    PENDING = _('sales.order.status.pending')
    READY_FOR_DELIVERY = _('sales.order.status.ready.for.delivery')
    SHIPPED = _('sales.order.status.shipped')
    CONFIRMED = _('sales.order.status.confirmed')
    CANCELED = _('sales.order.status.canceled')
    REFUNDED = _('sales.order.status.refunded')