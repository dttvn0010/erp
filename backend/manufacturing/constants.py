from django.utils.translation import gettext as _
from core.constants import TextEnum

class WorkCenterState(TextEnum):
    NORMAL = _('workcenter.state.normal')
    BLOCKED = _('workcenter.state.blocked')
    
class ProductionProcessStatus(TextEnum):
    DRAFT = _('production.status.draft')
    CONFIRMED = _('production.status.confirmed')
    PLANNED = _('production.status.planned')
    IN_PROGRESS = _('production.status.in.progress')
    DONE = _('production.status.done')
    CANCELED = _('production.status.canceled')

class ProductionStepStatus(TextEnum):
    NEW = _('production.step.status.new')
    IN_PROGRESS = _('production.step.status.in.progress')
    PAUSED = _('production.step.status.paused')
    DONE = _('production.step.status.done')
    CANCELED = _('production.step.status.canceled')

class DeviceMaintainanceStatus(TextEnum):
    DRAFT = _('device.maintainance.status.new')
    PLANNED = _('device.maintainance.status.planned')
    IN_PROGRESS = _('device.maintainance.in.progress')
    DONE = _('device.maintainance.done')
    CANCELED = _('device.maintainance.canceled')
    