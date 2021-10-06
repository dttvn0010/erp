from django.utils.translation import gettext as _
from core.constants import TextEnum

class InventoryStatus(TextEnum):
    DRAFT = _('inventory.status.draft')
    PLANNED = _('inventory.status.planned')
    DONE = _('inventory.status.done')
    CANCELED = _('inventory.status.canceled')