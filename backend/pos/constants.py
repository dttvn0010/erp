from core.constants import TextEnum
from django.utils.translation import gettext as _

class OrderStatus(TextEnum):
    DRAFT = _('pos.order.status.draft')
    PENDING = _('pos.order.status.pending')
    CONFIRMED = _('pos.order.status.confirmed')
    CANCELED = _('pos.order.status.canceled')
    RETURNED = _('pos.order.status.returned')

class OrderType(TextEnum):
    PURCHASE = _('pos.order.type.purchase')
    DISCOUNT = _('pos.order.type.discount')
    RETURN = _('pos.order.type.return')
