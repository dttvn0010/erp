from core.constants import TextEnum
from django.utils.translation import gettext as _

class OrderStatus(TextEnum):
    DRAFT = _('sales.order.status.draft')
    PENDING = _('sales.order.status.pending')
    CONFIRMED = _('sales.order.status.confirmed')
    CANCELED = _('sales.order.status.canceled')
    REFUNDED = _('sales.order.status.refunded')